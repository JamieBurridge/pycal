# Calendar
import calendar
import json
from datetime import datetime
from enum import Enum


DATE_FORMAT = "%Y-%m-%d"
filename = "events.json"

try:
    events = json.load(open(filename, "r"))
except FileNotFoundError:
    events = []
except ValueError:
    events = []


class Options(Enum):
    NEW = "new"
    ALL = "all"
    HELP = "help"


def main():
    options = {
        Options.NEW.value: {"description": "Create a new event."},
        Options.ALL.value: {"description": "Show all events."},
        Options.HELP.value: {"description": "Explains all options."}
    }

    is_done = False
    while not is_done:
        # Get user options (new event, delete event, see events)
        option = ""
        while option not in options.keys():
            option = input(f"What would you like to do? [new/all/help] ").lower()

        if option == Options.NEW.value:
            create_new_calendar_event()
        elif option == Options.ALL.value:
            show_all_events()
        elif option == Options.HELP.value:
            describe_options(options)

        is_done = check_if_done()

    print("Goodbye!")


def create_new_calendar_event():
    try:
        # Get user day, month and year
        user_day = get_int_input("Input a day: ")
        user_month = get_int_input("Input a month: ")
        user_year = get_int_input("Input a year: ")
        user_event = input("Input an event: ")

        # Check if in range
        cal_range = calendar.monthrange(user_year, user_month)
        if 1 <= user_day <= cal_range[1]:
            # Create datetime obj
            datetime_object = datetime(user_year, user_month, user_day)

            # Add to events list
            events.append(
                {
                    "id": len(events),
                    "event": user_event,
                    "date": datetime_object.strftime(DATE_FORMAT)
                })

            # Save to file
            with open(filename, "w", newline="") as file:
                json.dump(events, file)
        else:
            print("Incorrect date, please try again.")
            create_new_calendar_event()
    except ValueError:
        print("Incorrect date, please try again.")
        create_new_calendar_event()


def get_int_input(prompt):
    try:
        result = int(input(prompt))
        return result
    except ValueError:
        print("Value must be a number, please try again.")
        get_int_input(prompt)


def show_all_events():
    events_list = sort_datetime_list(events, "date")

    if len(events_list) == 0:
        print("You have not created any events")
    else:
        for event in events_list:
            print(f"{event['date']} | {event['event']}")


def sort_datetime_list(dt_list, key):
    return sorted(dt_list, key=lambda item: datetime.strptime(item[key], DATE_FORMAT).date())


def describe_options(options):
    for opt_key, opt_value in options.items():
        print(f"{opt_key} | {opt_value['description']}")


def check_if_done():
    answers = ["yes", "no"]
    answer = ""

    while answer.lower() not in answers:
        answer = input("Are you finished? [yes/no] ")

    return True if answer == "yes" else False


main()
