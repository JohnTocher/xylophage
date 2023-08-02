# xylophage
Log related tools reader and processor

Initial version reads a windows event viewer log,
specifically processing entries from the event viewer tree at:

> Applications and Service Logs  
> Microsoft  
> Windows  
> TerminalServices-RemoteConnectionManager  
> Operational  

It counts the number of entries and the totals for each user name

You will need a couple of settings in either your settings or secrets toml files:
Examples:
PATH_TO_LOGS = "D:/Somewhere"
CSV_LOG_FILE = "Log_example_2023-07-18.csv"
