import logging #logger is for the purpose that any execution happens we should be able to log all those information into some files
import os
from datetime import datetime

LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
logs_path = os.path.join(os.getcwd(), "logs", LOG_FILE)
os.makedirs(logs_path, exist_ok=True)   

LOG_FILE_PATH = os.path.join(logs_path, LOG_FILE)

logging.basicConfig(
    filename=LOG_FILE_PATH,
    format = "[%(asctime)s] %(lineno)d %(name)s - %(levelname)s - %(message)s",
    level = logging.INFO,
)

'''This Python code snippet is designed to create a logging system 
that writes logs to a file. Here's a brief explanation of its components:

LOG_FILE: Generates a log file name based on the current date and
 time, ensuring each log file has a unique name.
logs_path: Constructs a path for the log files by joining the 
current working directory with a "logs" folder and the log file
 name. This is intended to create a directory path, but there's
   a mistake in its implementation.
os.makedirs(logs_path, exist_ok=True): Attempts to create the 
directory path for the logs. The exist_ok=True parameter means it
 won't throw an error if the directory already exists. However, 
 this line is incorrectly trying to create a directory with the
   same name as the log file.
LOG_FILE_PATH: Intended to define the full path to the log file,
 but due to the earlier mistake, it redundantly joins the already
   complete logs_path with LOG_FILE, leading to an incorrect path.
logging.basicConfig(...): Configures the root logger to 
write logs to the file specified by LOG_FILE_PATH, with a
 specific format for log messages and a logging level of INFO.'''
