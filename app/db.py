from motor.motor_asyncio import AsyncIOMotorClient

MONGO_URI = "mongodb://localhost:27017"
client = AsyncIOMotorClient(MONGO_URI)

# 데이터베이스 및 컬렉션 설정
db = client["test"]
resData = db["restaurants"]
customerData = db["customers"]


resData.drop_indexes()

# 2dsphere 인덱스 생성
resData.create_index([("address.distance", "2dsphere")])