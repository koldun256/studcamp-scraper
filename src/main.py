from logger import Logger
from scraper import Scraper

url = "https://market.yandex.ru/card/krossovki-new-balance-530-beige-38eu/103170034668/reviews?do-waremd5=hNkC09vq5Refulmdc1cERA&sponsored=1&cpc=04EBqS6pRE6fCpwvkMjh8cd1mhzF3utVFH4iEn9Bgw_Ra9wNlC4Eq0o3syp80Z1-eupaZ6JTLjF4xang18xVQi3ggYIg4JpJBmBWzVKKx0wNPJw7584k6cFiOevvNFnm55Hh-vy6kjoaE-cvafDQnCZnP1WHXZ2IChbp7oh0QDQ6bd_E4Pwb4UeVsYL086I7qaDlLbf2pPjnL3BzhBh31YYffbfUl-8xi7Z01pGNqTsNzPZzos0vPdYrjPoUkAyaYf4LKHYzpx7A4hfjIK3qYT5RbIBO5RYfdTbg0-8IsZWsvUltQ74FZKKppr6eGz6s_8bpUuTehVMtkj1CVBvoQzUru774Ch9XygYxa9SS54RhpVwQtVdco1HtjpP6I7MnHijgX1s2-DL_ZofVxCk6cVoctZ9Ge-x7on2Ok643PZbqta6dZ9fsbDujrfx1x_g9j1dn9FNQrCYs77PHMXX6m5hMs6ZqYD19g9QZzgrJ_cArPfInAPtbkfenI-1VirInRDCHRPjd1_q5LcZ2qWfenS4KzsKgsH3MlpdlkCQsS0mjdxNeJe-BDe6jtc2N5Hn05gM1tgsypjWfaLT1t-Z9LQ%2C%2C"
url = "https://market.yandex.ru/card/krossovki-new-balance-530-beige-38eu"

logger = Logger()
scraper = Scraper(logger)

scraper.get(url)

reviews = []

for chunk in scraper.parse(30):
    reviews += chunk
    print(f"Got chunk of size {len(chunk)}")

scraper.quit()
