from datetime import datetime, timedelta, timezone
import os


SCOPES = ["https://www.googleapis.com/auth/calendar.readonly"]

WORK_START_HOUR = 9  # 9 AM
WORK_END_HOUR = 17  # 5 PM


def get_calendar_service():
    """Authenticate and return a Google Calendar service object."""
    try:
        from google.auth.transport.requests import Request
        from google.oauth2.credentials import Credentials
        from google_auth_oauthlib.flow import InstalledAppFlow
        from googleapiclient.discovery import build
    except ImportError as e:
        raise ImportError(
            "Google API libraries are required to access calendars. "
            "Install with: pip install google-auth google-auth-oauthlib google-api-python-client"
        ) from e

    creds = None
    if os.path.exists("token.json"):
        creds = Credentials.from_authorized_user_file("token.json", SCOPES)
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            creds.refresh(Request())
        else:
            flow = InstalledAppFlow.from_client_secrets_file("credentials.json", SCOPES)
            creds = flow.run_local_server(port=0)
        with open("token.json", "w") as token:
            token.write(creds.to_json())
    return build("calendar", "v3", credentials=creds)


def round_up_to_slot(dt: datetime, slot_length: int) -> datetime:
    """Round current datetime up to nearest slot boundary (30 or 60 minutes),
    respecting work hours."""
    dt = dt.astimezone(timezone.utc).replace(second=0, microsecond=0)

    # Minutes to add to get to the next slot
    remainder = dt.minute % slot_length
    if remainder != 0:
        dt += timedelta(minutes=(slot_length - remainder))

    # If before work hours → set to WORK_START_HOUR
    if dt.hour < WORK_START_HOUR:
        dt = dt.replace(hour=WORK_START_HOUR, minute=0)
    # If after work hours → roll to next day at WORK_START_HOUR
    elif dt.hour >= WORK_END_HOUR:
        dt = (dt + timedelta(days=1)).replace(hour=WORK_START_HOUR, minute=0)

    return dt


def within_work_hours(start: datetime, end: datetime) -> bool:
    # Convert to local timezone before checking and require the slot to
    # fully fall within the same day's working window [WORK_START_HOUR, WORK_END_HOUR).
    local_start = start.astimezone()
    local_end = end.astimezone()

    # Must be on the same local date
    if local_start.date() != local_end.date():
        return False

    # Define exact work window for that local date (end is exactly WORK_END_HOUR:00)
    work_start = local_start.replace(
        hour=WORK_START_HOUR, minute=0, second=0, microsecond=0
    )
    work_end = local_start.replace(
        hour=WORK_END_HOUR, minute=0, second=0, microsecond=0
    )

    # Slot must start at or after work_start and end at or before work_end
    return work_start <= local_start and local_end <= work_end


def find_free_slots(participants, slot_length, weeks):
    service = get_calendar_service()

    time_min = round_up_to_slot(datetime.now(timezone.utc), slot_length)
    time_max = time_min + timedelta(weeks=weeks)

    # Query busy times
    body = {
        "timeMin": time_min.isoformat(),
        "timeMax": time_max.isoformat(),
        "timeZone": "UTC",
        "items": [{"id": email} for email in participants],
    }

    freebusy_result = service.freebusy().query(body=body).execute()
    cal_dict = freebusy_result.get("calendars", {})

    # Gather busy intervals across all participants
    busy_intervals = []
    for _, data in cal_dict.items():
        for busy_time in data.get("busy", []):

            start = datetime.fromisoformat(
                busy_time["start"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)
            end = datetime.fromisoformat(
                busy_time["end"].replace("Z", "+00:00")
            ).astimezone(timezone.utc)

            busy_intervals.append((start, end))

    # Sort by start time
    busy_intervals.sort(key=lambda x: x[0])

    # Merge overlapping busy intervals
    merged_busy = []
    for interval in busy_intervals:
        if not merged_busy or interval[0] > merged_busy[-1][1]:
            merged_busy.append(list(interval))
        else:
            merged_busy[-1][1] = max(merged_busy[-1][1], interval[1])

    # Invert busy -> free intervals
    free_intervals = []
    cursor = time_min
    for start, end in merged_busy:
        if cursor < start:
            free_intervals.append((cursor, start))
        cursor = max(cursor, end)
    if cursor < time_max:
        free_intervals.append((cursor, time_max))

    # Slice free intervals into meeting slots
    meeting_slots = []
    slot_delta = timedelta(minutes=slot_length)
    for start, end in free_intervals:
        slot_start = start
        # Iterate through the free interval in slot-sized steps. Each candidate
        # slot is validated precisely by within_work_hours (which ensures the
        # slot does not end after WORK_END_HOUR).
        while slot_start + slot_delta <= end:
            slot_end = slot_start + slot_delta

            # Only add if fully inside working hours and on a weekday
            if slot_start.weekday() < 5 and within_work_hours(slot_start, slot_end):
                meeting_slots.append((slot_start, slot_end))

            slot_start = slot_end

    return meeting_slots
