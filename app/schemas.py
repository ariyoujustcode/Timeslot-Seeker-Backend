from pydantic import BaseModel


class TimeSlot(BaseModel):
    start: str
    end: str


class TimeslotRequest(BaseModel):
    participants: list[str]
    slot_length: int
    weeks: int


class TimeslotResponse(BaseModel):
    slots: list[TimeSlot]
