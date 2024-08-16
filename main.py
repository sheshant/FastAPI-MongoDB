import os
from datetime import datetime
from typing import List

import certifi
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
import motor.motor_asyncio


app = FastAPI(
    title="Wikipedia API",
    summary="A sample application showing how to use FastAPI to add a ReST API to a MongoDB collection.",
)
client = motor.motor_asyncio.AsyncIOMotorClient(
    "mongodb+srv://ssheshant:B3jFEPmcM0pkiE5K@test-cluster.hf6st.mongodb.net/college",
    tlsCAFile=certifi.where())
# client = motor.motor_asyncio.AsyncIOMotorClient(
#     "mongodb://localhost:27017/college")

db = client.college
collection = db.get_collection("wiki_records")


# Pydantic model for the items to be inserted
class Item(BaseModel):
    user_id: int
    article_id: int
    revision_id: int
    namespace: int
    timestamp: datetime
    md5: str
    reverted: int
    reverted_user_id: int
    reverted_revision_id: int
    delta: int
    cur_size: int


class BulkInsertResponse(BaseModel):
    message: str


@app.post("/items/bulk", response_model=BulkInsertResponse)
async def bulk_create_items(items: List[Item]):
    try:
        items_dict = [item.dict() for item in items]
        await collection.insert_many(items_dict)
        return BulkInsertResponse(message="Success")

    except Exception as e:
        print(e, e.__class__)
        raise HTTPException(status_code=500, detail=str(e))



