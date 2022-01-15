from datetime import datetime, time, timedelta
from typing import Optional, List
from uuid import UUID
from models import Lection, Item

from fastapi import Body, FastAPI, Header

app = FastAPI()

@app.post("/xxx", response_model=List[Lection])
async def ex1(arg: Lection):
    return arg,
