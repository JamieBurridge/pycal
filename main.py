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
    DEL = "del"
    HELP = "help"
    EXIT = "exit"


def main():
    options = {
        Options.NEW.value: {"description": "Create a new event."},
        Options.ALL.value: {"description": "Show all events."},
        Options.DEL.value: {"description": "Delete an event."},
        Options.HELP.value: {"description": "Explains all options."},
        Options.EXIT.value: {"description": "Exit the program."}
    }

    is_done = False
    while not is_done:
        # Get user options (new event, delete event, see events)
        option = ""
        while option not in options.keys():
            option = input(f"What would you like to do? {get_options_string()} ").lower()

        if option == Options.NEW.value:
            create_new_calendar_event()
        elif option == Options.ALL.value:
            show_all_events()
        elif option == Options.DEL.value:
            delete_event()
        elif option == Options.EXIT.value:
            is_done = True
        elif option == Options.HELP.value:
            describe_options(options)

    print("Goodbye!")


def get_options_string():
    options_list = [option.value for option in Options]
    options_string = "[" + "/".join(options_list) + "]"
    return options_string


def create_new_calendar_event():
    try:
        # Get user day, month and year
        user_day = get_int_input("Input a day: ")
        user_month = get_int_input("Input a month: ")
        user_year = get_int_input("Input a year: ", min_length=4)
        user_event = input("Input an event: ")

        # Check if in range
        cal_range = calendar.monthrange(user_year, user_month)
        if 1 <= user_day <= cal_range[1]:
            events.append({
                "id": len(events),
                "event": user_event,
                "date": datetime(user_year, user_month, user_day).strftime(DATE_FORMAT)
            })

            print("Event created successfully!")

            save_events(events)
        else:
            print("Incorrect date, please try again.")
            create_new_calendar_event()
    except ValueError:
        print("Incorrect date, please try again.")
        create_new_calendar_event()


def get_int_input(prompt, min_length=1):
    try:
        result = int(input(prompt))
        return result if len(str(result)) >= min_length else get_int_input(prompt)
    except ValueError:
        print("Value must be a number, please try again.")
        get_int_input(prompt)


def show_all_events(show_id=False):
    events_list = sort_datetime_list(events, "date")

    if len(events_list) == 0:
        print("You have not created any events")
    else:
        for event in events_list:
            if show_id:
                print(f"{event['id']} | {event['date']} | {event['event']}")
            else:
                print(f"{event['date']} | {event['event']}")


def sort_datetime_list(dt_list, key):
    return sorted(dt_list, key=lambda item: datetime.strptime(item[key], DATE_FORMAT).date())


def delete_event():
    global events

    show_all_events(show_id=True)
    delete_id = get_int_input("Which event do you want to delete? [number] ")

    events = [event for event in events if event["id"] != delete_id]
    save_events(events)


def save_events(new_events):
    with open(filename, "w", newline="") as file:
        json.dump(new_events, file)


def describe_options(options):
    for opt_key, opt_value in options.items():
        print(f"{opt_key} | {opt_value['description']}")


main()
