from datetime import datetime, timedelta, timezone
from main import within_work_hours


def test_simulated_interval():
    # Simulate local times 4:15pm - 5:15pm
    today_local = datetime.now().astimezone()
    free_start_local = today_local.replace(hour=16, minute=15, second=0, microsecond=0)
    free_end_local = today_local.replace(hour=17, minute=15, second=0, microsecond=0)

    free_start_utc = free_start_local.astimezone(timezone.utc)
    free_end_utc = free_end_local.astimezone(timezone.utc)

    slot_length = 60
    slot_delta = timedelta(minutes=slot_length)

    slots = []
    slot_start = free_start_utc
    while slot_start + slot_delta <= free_end_utc:
        slot_end = slot_start + slot_delta
        if within_work_hours(slot_start, slot_end):
            slots.append((slot_start, slot_end))
        slot_start = slot_end

    # Print results for manual inspection
    if not slots:
        print("PASS: No slots returned (none end before or at 5pm)")
    else:
        for s in slots:
            print(
                "FAIL: Slot returned ->",
                s[0].astimezone().strftime("%I:%M %p"),
                "-",
                s[1].astimezone().strftime("%I:%M %p"),
            )


if __name__ == "__main__":
    test_simulated_interval()
