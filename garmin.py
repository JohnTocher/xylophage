""" Functions for processing data from the Garmin world of web pages and logs 


"""

from datetime import datetime

WEEKDAY_NAMES = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]


def generate_date_from_day(input_day):
    """ Generates a long daye like 13 March 2024 from a single day like Thursday 
    
        Assumes the text was generated today and the activity was less than a week ago
        Assumes days wont be the same day
        ToDo - handle Yesterday
    """

    date_diff = False

    #date_today = datetime.now().strftime('%d %B %Y')
    day_today = datetime.now().strftime('%A')
    day_today = "Wednesday"

    print(f"Today is {day_today} and target is {input_day}")

    found_target = False
    found_today = False
    date_diff = False
    loop_index = 0

    for each_day in WEEKDAY_NAMES:
        loop_index += 1
        if each_day == day_today:
            if found_target:
                date_diff = found_target - loop_index
                print(f"Finishing with today: {loop_index}")
                break
            else:
                found_today = loop_index
                print(f"Today: {found_today}")
        elif each_day == input_day:
            if found_today:
                print(f"Finishing with target: {loop_index}")
                date_diff = (7 - (loop_index - found_today)) * -1
                break
            else:
                found_target = loop_index
                print(f"Target: {found_target}")

    return date_diff




def parse_garmin_run(summary_text_list):
    """ Iterates over the provided list of text, returns dictionary of data

    """

    data_dict = dict()
    data_dict["error"] = True
    list_length = len(summary_text_list)

    #if list_length != 15:
    #    data_dict["message"] = f"Unexpected number of lines: {len(summary_text_list)}"
    #    return data_dict

    first_line = summary_text_list[0]
    if first_line.startswith("Running"):
        date_boundary_right = first_line.rfind("@")
        date_boundary_left = first_line.rfind("on")
        data_part = first_line[date_boundary_left+3:date_boundary_right].strip()
        if data_part in WEEKDAY_NAMES:
            data_part = generate_date_from_day(date_part)

        data_dict["date text"] = data_part
        time_text = first_line[date_boundary_right+2:].strip()
        data_dict["start time"] = time_text
    else:
        data_dict["message"] = f"Not a run {first_line}"
        return data_dict

    # Get distance from text like: 5.39 km
    current_desc = summary_text_list[6]
    current_data = summary_text_list[5]
    if current_desc == "Distance":
        data_dict["distance"] = float(current_data.split(" ")[0])
    else:
        data_dict["message"] = f"Missing distance: {current_desc}"
        return data_dict
    
    # Get time from text like: 23:49
    current_desc = summary_text_list[8]
    current_data = summary_text_list[7]
    if current_desc == "Time":
        data_dict["time"] = current_data
    else:
        data_dict["message"] = f"Missing time: {current_desc}"
        return data_dict
 

    # Get pace from text like: 6:35 /km
    current_desc = summary_text_list[10]
    current_data = summary_text_list[9]
    if current_desc == "Avg Pace":
        data_dict["avg pace"] = current_data.split(" ")[0]
    else:
        data_dict["message"] = f"Missing pace: {current_desc}"
        return data_dict
    
    # Get ascent from text like: 22 m
    current_desc = summary_text_list[12]
    current_data = summary_text_list[11]
    if current_desc == "Total Ascent":
        data_dict["total ascent"] = int(current_data.split(" ")[0])
    else:
        data_dict["message"] = f"Missing ascent: {current_desc}"
        return data_dict

    # Get calories from text like: 301
    current_desc = summary_text_list[14]
    current_data = summary_text_list[13]
    if current_desc == "Calories":
        data_dict["calories"] = int(current_data.split(" ")[0])
    else:
        data_dict["message"] = f"Missing calories: {current_desc}"
        return data_dict
    
    # Search the rest of the lines for the next field we expect
    current_line = 14
    search_for = "Avg HR"   # Looks like: 135 bpm
    search_ok = False
    last_line = "Empty"
    while current_line < list_length:
        this_line = summary_text_list[current_line]
        if this_line == search_for:
            data_dict[search_for] = int(last_line.split(" ")[0])
            search_ok = True
            break
        else:
            last_line = this_line
            current_line += 1
    if not search_ok:
        data_dict["message"] = f"Missing {search_for}: {last_line}"
        return data_dict

    search_for = "Max HR"   # Looks like: 155 bpm
    search_ok = False
    last_line = "Empty"
    while current_line < list_length:
        this_line = summary_text_list[current_line]
        if this_line == search_for:
            data_dict[search_for] = int(last_line.split(" ")[0])
            search_ok = True
            break
        else:
            last_line = this_line
            current_line += 1
    if not search_ok:
        data_dict["message"] = f"Missing {search_for}: {last_line}"
        return data_dict
    

    data_dict["error"] = False
    return data_dict

def garmin_data_for_clipboard(garmin_dict):
    """ Generates the text to put on the clipboard for pasting into a spreadsheet
    
    
        Interprests the garmin data dictionary and formats it for what ought to work
        pasted into google sheets
    """
    date_format = "%d %B %Y"
    clip_text = ""
    start_time = datetime.strptime(garmin_dict["date text"], date_format)

    clip_text = start_time.strftime('%d/%m/%Y')
    clip_text = f"{clip_text}\t{garmin_dict['start time']}"
    clip_text = f"{clip_text}\t{garmin_dict['distance']}"
    clip_text = f"{clip_text}\t00:{garmin_dict['time']}"
    clip_text = f"{clip_text}\t{garmin_dict['calories']}"
    clip_text = f"{clip_text}\t{garmin_dict['Avg HR']}"
    clip_text = f"{clip_text}\t{garmin_dict['Max HR']}"
    #print(f"Text is [{clip_text}]")

    return clip_text