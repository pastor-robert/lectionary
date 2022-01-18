from pydantic import BaseModel, Field, validator, root_validator
from typing import List
from typing import Optional, Set
from pydantic import BaseModel
from enum import Enum
from datetime import date
from bson import ObjectId


class PyObjectId(ObjectId):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if not ObjectId.is_valid(v):
            raise ValueError("Invalid objectid")
        return ObjectId(v)

    @classmethod
    def __modify_schema__(cls, field_schema):
        field_schema.update(type="string")

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


class LectionInput(BaseModel):
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

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        underscore_attrs_are_private = True

class Lection(LectionInput):
    id: PyObjectId = Field(default_factory=PyObjectId, alias="_id")

    class Config:
        allow_population_by_field_name = True
        arbitrary_types_allowed = True
        json_encoders = {ObjectId: str}
        underscore_attrs_are_private = True
