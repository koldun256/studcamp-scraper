from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel
from logger import Logger
from scraper import Scraper

app = FastAPI(
    title="Парсер отзывов с Яндекс.Маркета",
    description="API для парсинга отзывов с карточек товаров на Яндекс.Маркете"
)

class ParseResponse(BaseModel):
    url: str
    reviews_count: int
    reviews: list

logger = Logger()

@app.get("/api/v1/parse_url", response_model=ParseResponse)
async def parse_url(
    url: str = Query(..., description="URL карточки товара на Яндекс.Маркете"),
    limit: int = Query(30, description="Лимит количества отзывов для парсинга")
):
    """
    Парсит отзывы с указанного URL Яндекс.Маркета
    
    - **url**: URL карточки товара (обязательный параметр)
    - **limit**: Лимит количества отзывов (по умолчанию 30)
    """
    try:
        scraper = Scraper(logger)
        
        scraper.get(url)
        
        reviews = []
        for chunk in scraper.parse(limit):
            reviews += chunk
        
        scraper.quit()
        
        return {
            "url": url,
            "reviews_count": len(reviews),
            "reviews": reviews
        }
        
    except Exception as e:
        logger.log(f"Error parsing URL {url}: {str(e)}", Logger.Level.Error)
        raise HTTPException(
            status_code=400,
            detail=f"Error parsing URL: {str(e)}"
        )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)