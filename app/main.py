from fastapi import FastAPI
from app.routers import review_router

app = FastAPI()

# 라우터 등록
app.include_router(review_router, prefix="/reviews", tags=["Reviews"])

@app.get("/")
def read_root():
    return {"message": "Welcome to the FastAPI & Elasticsearch integration!"}
