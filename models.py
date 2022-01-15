from pydantic import BaseModel, Field, validator, root_validator
from typing import List
from typing import Optional, Set

from fastapi import FastAPI
from pydantic import BaseModel
from enum import Enum
from datetime import date


class Season(str, Enum):
    advent = "Advent"
    christmas = "Christmas"
    epiphany = "Ephiphany"
    lent = "Lent"
    easter = "Easter"
    pentecost = "Pentecost"
    ordinary = "Ordinary"

class Year(str, Enum):
    A = "A"
    B = "B"
    C = "C"

class Readings(BaseModel):
    first: str = Field(..., title="First Reading", example="Isaiah 2:1-5")
    psalm: str = Field(..., title="Psalm", example="Psalm 122")
    second: str = Field(..., title="Second Reading", example="Romans 13:11-14")
    gospel: str = Field(..., title="Gospel", example="Matthew 24:36-44")

class LectionaryDate(BaseModel):
    year: Year
    season: Season
    ordinal: int = None

class Lection(BaseModel):
    lectionary_date: Optional[LectionaryDate] = None
    calendar_date: Optional[date] = None
    short_name: str = Field(..., title="Short Name", example="Advent1A")
    long_name: str = Field(..., title="Long Name", example="First Sunday of Advent, Year A")
    readings: Readings = Field(..., description="Semicontinuous during Ordinary Sundays")
    alt_readings: Readings = Field(None, description="Complementary during Ordinary Sundays")

    @root_validator
    def exactly1date(cls, values):
        calendar_date = values.get('calendar_date')
        lectionary_date = values.get('lectionary_date')
        #print(f"exactly1date: I: {calendar_date}/{lectionary_date}/{v}/{values}")
        if calendar_date and lectionary_date:
            raise ValueError("must not specify both dates")
        if not ( calendar_date or lectionary_date ):
            raise ValueError("must specify a date")
        return values


class Image(BaseModel):
    url: str
    name: str


class Item(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    tax: Optional[float] = None
    tags: Set[str] = []
    image: Optional[Image] = None
