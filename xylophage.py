# import csv
import pyperclip
from config import settings

# import rich # Don't need this *yet*
from pathlib import Path
from datetime import datetime

from garmin import parse_garmin_run
from garmin import garmin_data_for_clipboard
from garmin import generate_date_from_day

def read_file_into_list(file_to_read):
    """ Reads the provided file into a list object 
    
        Reads each line into a list ibect, removing whitespace at both ends
        Possibly not the best option for massive files!    
    """

    line_list = list()

    with open(file_to_read, "r") as input_file:
        line_list = [raw_line.strip() for raw_line in input_file.readlines()]
    
    return line_list



def read_event_log():
    """Read a windows event log formatted as csv

    Extracted from event manager:
    > Applications and Service Logs
    > Microsoft
    > Windows
    > TerminalServices-RemoteConnectionManager
    > Operational
    """

    count_lines = 0
    count_events = 0
    count_user = 0
    user_details = dict()

    log_filename = Path(settings.path_to_logs) / settings.csv_log_file

    with open(log_filename, "r") as log_file:
        for each_line in log_file:
            count_lines += 1
            if each_line.startswith("User:"):
                count_user += 1
                user_name = each_line[5:].strip().upper()
                user_count = user_details.get(user_name, 0)
                user_details[user_name] = user_count + 1

    print(f"Processed {log_filename}")
    print(f"Found {count_lines} lines and {count_events} events")
    print(f"Found {count_user} user events")
    print(f"Users {user_details}")

    return count_events


def process_garmin_data():
    """ try reading some garmin data
    """

    input_filename = Path(settings.GARMIN_FOLDER) / settings.GARMIN_INPUT
    print(f"Trying to read from: {input_filename}")
    garmin_raw = read_file_into_list(input_filename)
    print(f"Read {len(garmin_raw)} lines")
    garmin_data = parse_garmin_run(garmin_raw)
    print(f"Garmin data: {garmin_data}")
    clipboard_text = garmin_data_for_clipboard(garmin_data)
    pyperclip.copy(clipboard_text)
    print(f"Clipboard: [{clipboard_text}]")

def run_main():
    """Main function for custom and one-off runs"""

    #read_result = read_event_log()
    #read_result = process_garmin_data()
    test_value = generate_date_from_day("Thursday")
    print(f"{test_value}")



if __name__ == "__main__":
    run_main()
