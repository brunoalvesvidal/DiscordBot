from motor.motor_asyncio import AsyncIOMotorClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGODB_URI = os.getenv("MONGODB_URI")
DB_NAME = os.getenv("MONGODB_DB")

if not MONGODB_URI:
    raise RuntimeError("MONGODB_URI nao definido no .env")

if not DB_NAME:
    raise RuntimeError("MONGODB_DB nao definido no .env")

client = AsyncIOMotorClient(MONGODB_URI)
db = client[DB_NAME]

suportes_collection = db["Suporte"]


async def insert_suporte(suporte_data: dict):
    result = await suportes_collection.insert_one(suporte_data)
    return result.inserted_id


async def get_suporte_by_id(suporte_id: int):
    return await suportes_collection.find_one({"suporte_id": suporte_id})


async def close_suporte(suporte_id: int, responsavel: str) -> bool:
    result = await suportes_collection.update_one(
        {"suporte_id": suporte_id, "status": "open"},
        {"$set": {"status": "closed", "responsavel": responsavel}},
    )
    return result.modified_count > 0


async def count_suportes() -> int:
    return await suportes_collection.count_documents({})

