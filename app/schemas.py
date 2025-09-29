from typing import List
from pydantic import BaseModel, Field, EmailStr
from datetime import datetime


class TimeSlot(BaseModel):
    start: datetime
    end: datetime


class TimeslotRequest(BaseModel):
    participants: List[EmailStr]
    slot_length: int = Field(..., ge=5, le=480)  # 0–480 minutes
    weeks: int = Field(..., ge=1, le=4)  # 1–4 weeks only


class TimeslotResponse(BaseModel):
    slots: List[TimeSlot]
