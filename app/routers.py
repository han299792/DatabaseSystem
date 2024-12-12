from fastapi import APIRouter, HTTPException
from app.models import Review
from app.services import create_index, insert_review, search_reviews
import json

review_router = APIRouter()
# 인덱스 생성
@review_router.on_event("startup")
async def startup_event():
    create_index()

# JSON 파일의 데이터를 Elasticsearch에 로드
@review_router.post("/load")
async def load_reviews():
    try:
        with open("app/reviews.json", "r", encoding="utf-8") as f:
            reviews = json.load(f)
            for review in reviews:
                insert_review(review)
        return {"message": "Reviews loaded into Elasticsearch successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# 텍스트 검색
@review_router.get("/search/")
async def search_review(query: str):
    try:
        results = search_reviews(query)
        return {"results": results["hits"]["hits"]}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
