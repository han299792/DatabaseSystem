from elasticsearch import Elasticsearch
from fastapi import FastAPI
from routes import router

app = FastAPI()
print(1)
app.include_router(router)
es = Elasticsearch("http://localhost:9200")
@app.get("/")
async def root():
    return {"message": "FastAPI 서버 실행중"}
