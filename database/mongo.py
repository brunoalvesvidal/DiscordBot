from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

suportes_collection = db["suportes"]

async def insert_suporte(suporte_data):
    result = await suportes_collection.insert_one(suporte_data)
    return result.inserted_id

async def get_suporte_by_id(suporte_id):
    return await suportes_collection.find_one({"_id": suporte_id})

async def close_suporte(suporte_id):
    result = await suportes_collection.update_one(
        {"_id": suporte_id},
        {"$set": {"status": "closed"}}
    )
    return result.modified_count
