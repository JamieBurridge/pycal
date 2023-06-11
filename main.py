# Calendar
import calendar
import json

filename = "events.json"

try:
    events = json.load(open(filename, "r"))
except:
    events = []


def main():
    # Get user options (new event, delete event, see events)

    # Get user day, month and year
    user_day = int(input("Input a day: "))
    user_month = int(input("Input a month: "))
    user_year = int(input("Input a year: "))
    user_event = input("Input an event: ")

    # Check if day, month and year is valid
    try:
        cal_range = calendar.monthrange(user_year, user_month)
        if 1 <= user_day <= cal_range[1]:
            events.append(
                {
                    "id": len(events),
                    "event": user_event,
                    "date": {"day": user_day, "month": user_month, "year": user_year}
                })
            print(events)

            with open(filename, "w", newline="") as file:
                json.dump(events, file)
    except:
        print("Wrong")


main()
