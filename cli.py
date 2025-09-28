from tabulate import tabulate
from app.logic import find_free_slots


def get_user_input():
    print("Welcome to Timeslot Seeker!\n")

    users_input = input("Enter participant emails, separated by commas: ")
    participants = [u.strip() for u in users_input.split(",")]

    while True:
        length_input = input("Enter meeting length (30 or 60 minutes): ")
        if length_input in ["30", "60"]:
            slot_length = int(length_input)
            break
        print("Invalid input. Please enter 30 or 60.")

    while True:
        weeks_input = input("Enter time period (1, 2, 3, or 4 weeks): ")
        if weeks_input in ["1", "2", "3", "4"]:
            weeks = int(weeks_input)
            break
        print("Invalid input. Please enter 1, 2, 3, or 4.")

    return participants, slot_length, weeks


def main():
    participants, slot_length, weeks = get_user_input()
    print("Participants:", participants, "\n")
    print("Slot length:", slot_length, "minutes\n")
    print("Timespan:", weeks, "weeks\n")
    print("\nFinding available meeting slots...\n")

    slots = find_free_slots(participants, slot_length, weeks)

    if not slots:
        print("No common free slots found.")
        return

    table = []

    for s in slots:
        local_start = s[0].astimezone()
        local_end = s[1].astimezone()

        table.append(
            [
                local_start.strftime("%m/%d/%y"),
                local_start.strftime("%A"),
                f"{local_start.strftime('%I:%M %p')} - {local_end.strftime('%I:%M %p')}",
            ]
        )

    print(tabulate(table, headers=["Date", "Day", "Time"], tablefmt="grid"))


if __name__ == "__main__":
    main()
