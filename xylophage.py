import csv
from config import settings

# import rich # Don't need this *yet*
from pathlib import Path


def read_event_log():
    """Read a windows event log formatted as csv"""

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


def run_main():
    """Main function for custom and one-off runs"""

    read_result = read_event_log()


if __name__ == "__main__":
    run_main()
