# Import Python's built-in logging module
# Logging is used to record events that happen during program execution.
# Instead of printing messages on the screen, logging stores them in a file.
import logging

# Import os module
# This module helps us interact with the operating system,
# such as creating folders and handling file paths.
import os

# Import datetime class to work with date and time
# We will use this to create unique log file names based on time.
from datetime import datetime


# Create a log file name using the current date and time
# strftime() formats the time.
# Example output: 03_15_2026_10_45_30.log
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"


# Create the path where logs will be stored
# os.getcwd() → gives the current working directory of the project
# "logs" → folder where log files will be saved
# LOG_FILE → the name of the log file created above
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)


# Create the directory if it does not already exist
# exist_ok=True prevents an error if the folder already exists
os.makedirs(logs_path, exist_ok=True)


# Create the full path of the log file
# This joins the folder path and file name
LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)


# Configure the logging system
logging.basicConfig(

    # File where logs will be written
    filename=LOG_FILE_PATH,

    # Format of each log message
    # %(asctime)s  → timestamp when log was created
    # %(lineno)d   → line number in the code where log was generated
    # %(name)s     → module name
    # %(levelname)s → type of log (INFO, WARNING, ERROR, etc.)
    # %(message)s  → actual log message
    format="[ %(asctime)s ] %(lineno)d %(name)s - %(levelname)s - %(message)s",

    # Logging level
    # INFO means it will record logs with level INFO and above
    # (INFO, WARNING, ERROR, CRITICAL)
    level=logging.INFO
)


'''
This block is commented out.

Normally this block checks if the file is executed directly
and then writes a log message saying logging has started.

if __name__ == "__main__":
    logging.info("Logging has started")
But since it is inside triple quotes, it will NOT execute.
'''