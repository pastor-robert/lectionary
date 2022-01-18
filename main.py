from datetime import datetime, time, timedelta
from typing import Optional, List
from uuid import UUID
from models import Lection, LectionInput

from fastapi import Body, FastAPI, Header, status, HTTPException
from fastapi.responses import JSONResponse
from fastapi.encoders import jsonable_encoder

from google.cloud import secretmanager

import motor.motor_asyncio

import os


client = None
db = None
app = FastAPI()


@app.get("/env")
async def env():
    return os.environ

@app.post(
    "/",
    response_model_exclude_none=True,
    response_description="Add a lection",
    response_model=Lection)
async def create_lection(lection: LectionInput):
    #print(f"create_date: I: type(lection)={type(lection)}, lection={lection}")
    lection = jsonable_encoder(lection)
    #print(f"create_date: II: type(lection)={type(lection)}, lection={lection}")
    new_lection = await db["lectionary"].insert_one(lection)
    #print(f"create_date: III: new_lection={new_lection}")
    created_lection = await db["lectionary"].find_one({"_id": new_lection.inserted_id})
    #print(f"create_date: IV: created_lection={created_lection}")
    return JSONResponse(status_code=status.HTTP_201_CREATED, content=created_lection)


@app.get(
    "/",
    response_model_exclude_none=True,
    response_description="List all lections",
    response_model=List[Lection])
async def read_lections():
    dates = await db["lectionary"].find().to_list(1000)
    return dates

@app.get(
    "/{id}",
    response_model_exclude_none=True,
    response_description="List a single lection",
    response_model=Lection)
async def create_lections(id: str):
    lection = await db["lectionary"].find_one({"_id": id})
    if(lection):
        return lection
    raise HTTPException(status_code=404, detail=f"Lection {id} not found")

@app.delete(
    "/{id}",
    response_model_exclude_none=True,
    response_description="Delete a lection")
async def delete_student(id: str):
    delete_result = await db["lectionary"].delete_one({"_id": id})

    if delete_result.deleted_count == 1:
        return JSONResponse(status_code=status.HTTP_204_NO_CONTENT)

    raise HTTPException(status_code=404, detail=f"Student {id} not found")

async def connect_db():
    global client
    global db
    url = get_secret("MONGODB_URL")
    client = motor.motor_asyncio.AsyncIOMotorClient(url)
    db = client.lectionary
app.add_event_handler("startup", connect_db)

def get_secret(
        name:str,
        version:str = "latest",
        project_id:str = os.environ.get("GOOGLE_CLOUD_PROJECT")
        ) -> str:
    service = secretmanager.SecretManagerServiceClient()
    name = f"projects/{project_id}/secrets/{name}/versions/{version}"
    request = {"name": name}
    secret = service.access_secret_version(request=request)
    return secret.payload.data.decode("utf-8")
