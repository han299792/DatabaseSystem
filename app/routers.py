from fastapi import APIRouter, HTTPException
from app.models import Review
from app.services import create_index, insert_review, search_reviews
import json
from app.db import customerData, resData
from bson import ObjectId

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
    try:
        with open("app/data/test.Customer.json", "r", encoding="utf-8") as file:
            data = json.load(file)
            for item in data:
                # `_id` 필드가 `$oid` 형식일 경우 ObjectId로 변환
                if "_id" in item and "$oid" in item["_id"]:
                    item["_id"] = ObjectId(item["_id"]["$oid"])
                
                # 중복 확인 및 데이터 삽입
                existing = await customerData.find_one({"_id": item["_id"]})
                if not existing:
                    await customerData.insert_one(item)
        return {"message": "Customer data loaded successfully."}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
@review_router.get("/find_nearby_restaurants")
async def find_nearby_restaurants():
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
                        "maxDistance": 5000,  # 5km
                        "spherical": True
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

