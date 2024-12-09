from fastapi import APIRouter, HTTPException
from database import database
from models import reviews

router = APIRouter()

@router.post("/reviews/")
async def create_review(content: str, rating: int):
    query = reviews.insert().values(content=content, rating=rating)
    try:
        await database.execute(query)
        return {"message": "리뷰가 성공적으로 추가되었습니다!"}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
    
@router.get("/reviews/")
async def read_reviews():
    query = reviews.select()
    return await database.fetch_all(query)
