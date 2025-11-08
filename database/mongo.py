from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")

client = AsyncIOMotorClient(MONGO_URI)
db = client[DB_NAME]

tickets_collection = db["tickets"]

async def insert_ticket(ticket_data):
    result = await tickets_collection.insert_one(ticket_data)
    return result.inserted_id

async def get_ticket_by_id(ticket_id):
    return await tickets_collection.find_one({"_id": ticket_id})

async def close_ticket(ticket_id):
    result = await tickets_collection.update_one(
        {"_id": ticket_id},
        {"$set": {"status": "closed"}}
    )
    return result.modified_count
