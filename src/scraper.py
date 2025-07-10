from time import sleep
from typing import Generator

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options

from logger import Logger
from review import Review
from scraper_logger import ScraperLogger

class Scraper:
    __logger: ScraperLogger

    def __init__(self, logger: Logger, options=Options()):
        options.add_argument("--headless=new")
        self.__driver = webdriver.Chrome(options)
        self.__logger = ScraperLogger(logger)

    def get(self, url: str) -> None:
        self.__logger.get_begin(url)
        try:
            self.__driver.get(url)
            self.__logger.get_successful()
        except Exception as e:
            self.__logger.get_fail(e)
            raise

    def __scroll(self) -> int:
        def get_height():
            return self.__driver.execute_script("return document.body.scrollHeight")
        
        self.__driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        return get_height()
    
    def __parse_review(self, review_el) -> Review:
        review_id = None

        try:
            review_id = review_el.find_element(By.XPATH, ".//*[@data-auto='review-item']").get_attribute('id')
            review_body = review_el.find_element(By.XPATH, ".//*[@itemprop='reviewBody']").get_attribute('content')
            date = review_el.find_element(By.XPATH, ".//*[@itemprop='datePublished']").get_attribute('content')
            rating = review_el.find_element(By.XPATH, ".//*[@itemprop='ratingValue']").get_attribute('content')
            likes = review_el.find_element(By.XPATH, ".//*[@data-auto='like-button']").text
            dislikes = review_el.find_element(By.XPATH, ".//*[@data-auto='dislike-button']").text
            profile_name = review_el.find_element(By.XPATH, ".//*[@data-auto='nickname']").text

            profile_url = ""

            try:
                profile_url = review_el.find_element(By.XPATH, ".//*[@data-zone-name='profile']/a").get_attribute('href')
            except Exception as e:
                self.__logger.report_no_url()
            

            profile_image_url = review_el.find_element(By.XPATH, ".//*[@data-auto='avatar']").get_attribute('src')

            return Review(
                review_id=review_id,
                review_body=review_body,
                date=date,
                rating=rating,
                likes=likes,
                dislikes=dislikes,
                profile_name=profile_name,
                profile_url=profile_url,
                profile_image_url=profile_image_url
            )

        except Exception as e:
            self.__logger.review_parse_fail(e, review_id)
            raise

    def __parse_chunk(self, chunk_el, limit) -> list[Review]:
        reviews = []
        review_els = chunk_el.find_elements(By.XPATH, ".//*[@data-zone-name='review']")

        for review_el in review_els:
            if limit is not None and len(reviews) >= limit:
                break

            try:
                reviews.append(self.__parse_review(review_el))
            except Exception as e:
                pass

        return reviews

    def __chunk_iter(self):
        last_chunk_selector = "[data-apiary-widget-name=\"@card/ReviewsLayout\"]:last-child"

        prev_chunk = None

        while True:
            try:
                new_chunk = self.__driver.find_element(By.CSS_SELECTOR, last_chunk_selector)
            except Exception as e:
                self.__logger.chunks_parse_fail(e)
                raise

            if new_chunk == prev_chunk:
                return

            yield new_chunk

            self.__scroll()

    def parse(self, limit=None) -> Generator[list[Review], None, None]:
        parsed_count = 0

        for chunk in self.__chunk_iter():
            parsed_reviews = self.__parse_chunk(chunk, None if limit is None else limit - parsed_count)

            self.__logger.progress(len(parsed_reviews))
            parsed_count += len(parsed_reviews)

            yield parsed_reviews

            if limit is not None and parsed_count >= limit:
                return

    def quit(self):
        self.__logger.finish()
        self.__driver.quit()