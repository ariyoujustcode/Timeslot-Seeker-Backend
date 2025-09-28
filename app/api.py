from fastapi import APIRouter
from .logic import find_free_slots
from .schemas import TimeSlot, TimeslotRequest, TimeslotResponse

router = APIRouter()


@router.post("/find-timeslot", response_model=TimeslotResponse)
def find_timeslot_endpoint(req: TimeslotRequest):
    slots = find_free_slots(req.participants, req.slot_length, req.weeks)

    # Create TimeSlot objects instead of plain dicts
    formatted = [TimeSlot(start=s[0].isoformat(), end=s[1].isoformat()) for s in slots]

    return TimeslotResponse(slots=formatted)


@router.post("/test-slots")
def test_slots(req: TimeslotRequest):
    slots = find_free_slots(req.participants, req.slot_length, req.weeks)

    preview = []
    for s in slots[:10]:  # show just first 10 slots
        preview.append(
            {
                "utc_start": s[0].isoformat(),
                "utc_end": s[1].isoformat(),
                "local_start": s[0].astimezone().strftime("%Y-%m-%d %I:%M %p"),
                "local_end": s[1].astimezone().strftime("%Y-%m-%d %I:%M %p"),
            }
        )

    return {"preview_slots": preview}
