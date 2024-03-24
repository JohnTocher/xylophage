""" Functions for processing data from the Garmin world of web pages and logs 


"""

def parse_garmin_run(summary_text_list):
    """ Iterates over the provided list of text, returns dictionary of data

    """

    data_dict = dict()
    data_dict["error"] = True

    if len(summary_text_list) != 15:
        data_dict["message"] = f"Unexpected number of lines: {len(summary_text_list)}"
        return data_dict

    first_line = summary_text_list[0]
    if first_line.startswith("Running"):
        date_boundary_right = first_line.rfind("@")
        date_boundary_left = first_line.rfind("on")
        data_part = first_line[date_boundary_left+3:date_boundary_right].strip()
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

    data_dict["error"] = False
    return data_dict