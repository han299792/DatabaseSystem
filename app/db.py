from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)

# 데이터베이스 및 컬렉션 설정
db = client["business_data"]
resData = db["restaurants"]
customerData = db["customers"]
