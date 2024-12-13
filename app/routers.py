from fastapi import APIRouter, HTTPException
from app.models import Review
from app.services import create_index, insert_review, search_reviews
import json
from app.db import customerData, resData
from bson import ObjectId
import sqlite3
import json
from elasticsearch import Elasticsearch

# Elasticsearch 설정
es = Elasticsearch(hosts=["http://localhost:9200"])

# FastAPI Router
review_router = APIRouter()

# SQLite DB 파일 경로
DB_PATH = "hw4.db"

# Elasticsearch Index 이름
INDEX_NAME = "reviews"

# Elasticsearch 인덱스 생성 함수
def create_index():
    if not es.indices.exists(index=INDEX_NAME):
        es.indices.create(
            index=INDEX_NAME,
            body={
                "mappings": {
                    "properties": {
                        "review_id": {"type": "keyword"},
                        "rec_id": {"type": "keyword"},
                        "author": {"type": "text"},
                        "content": {"type": "text"}
                    }
                }
            }
        )
        print(f"Index '{INDEX_NAME}' created.")

@review_router.on_event("startup")
async def startup_event():
    # Elasticsearch 인덱스 생성
    create_index()

@review_router.post("/load")
async def load_reviews_from_db():
    """
    SQLite DB에서 데이터를 읽어와 JSON 형식으로 변환 후 Elasticsearch에 저장.
    """
    try:
        # SQLite DB 연결
        conn = sqlite3.connect(DB_PATH)
        cursor = conn.cursor()

        # Review 테이블의 데이터 읽기
        cursor.execute("SELECT review_id, rec_id, author, content FROM Review")
        rows = cursor.fetchall()

        # 데이터를 Elasticsearch에 삽입
        for row in rows:
            review = {
                "review_id": row[0],
                "rec_id": row[1],
                "author": row[2],
                "content": row[3]
            }
            es.index(index=INDEX_NAME, id=review["review_id"], body=review)

        conn.close()
        return {"message": "Reviews loaded into Elasticsearch successfully."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading reviews: {str(e)}")

@review_router.get("/search/")
async def search_review(query: str):
    """
    특정 쿼리와 일치하는 텍스트가 포함된 리뷰 데이터를 반환.
    """
    try:
        # Elasticsearch 검색 쿼리
        results = es.search(
            index=INDEX_NAME,
            body={
                "query": {
                    "match": {
                        "content": query
                    }
                }
            }
        )
        return {"results": [hit["_source"] for hit in results["hits"]["hits"]]}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error searching reviews: {str(e)}")

@review_router.post("/load/restaurants/")
async def load_restaurants():
    try:
        with open("app/data/test.Restaurant.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                # `_id` 필드가 `$oid` 형식일 경우 ObjectId로 변환
                if "_id" in item and "$oid" in item["_id"]:
                    item["_id"] = ObjectId(item["_id"]["$oid"])
                
                # 중복 확인 및 데이터 삽입
                existing = await resData.find_one({"_id": item["_id"]})
                if not existing:
                    await resData.insert_one(item)
        return {"message": "Restaurant data loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@review_router.post("/load/customers/")
async def load_customers():
    """
    JSON 데이터를 MongoDB에 삽입하는 API.
    """
    try:
        with open("app/data/test.Customer.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            success_count = 0  

            for item in data:
                if "_id" in item and "$oid" in item["_id"]:
                    item["_id"] = ObjectId(item["_id"]["$oid"])
                
                existing = await customerData.find_one({"_id": item["_id"]})
                if not existing:
                    result = await customerData.insert_one(item)
                    if result.inserted_id:
                        success_count += 1

        return {"message": f"Customer data loaded successfully. {success_count} records inserted."}

    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error loading customers: {str(e)}")
    
@review_router.get("/find_nearby_restaurants")
async def find_nearby_restaurants():
    """
    각 고객의 위치를 기준으로 가까운 레스토랑을 검색하는 API.
    """
    try:
        customer_name = []
        customer_address = []

        async for doc in customerData.find():
            if 'address' in doc and 'distance' in doc['address']:
                customer_name.append(doc['cus_name'])
                customer_address.append(doc['address']['distance']['coordinates'])

        result = []

        for i, customer in enumerate(customer_address):
            customer_lon, customer_lat = customer
            cursor = resData.aggregate([
                {
                    "$geoNear": {
                        "near": {
                            "type": "Point",
                            "coordinates": [customer_lon, customer_lat]
                        },
                        "distanceField": "distance",
                        "maxDistance": 5000,  
                        "spherical": True,
                        "key": "address.distance"
                    }
                }
            ])
            async for doc in cursor:
                result.append({
                    "Customer": customer_name[i],
                    "Restaurant": doc['name'],
                    "Distance": f"{doc['distance']:.2f} meters"
                })

        return {"data": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))