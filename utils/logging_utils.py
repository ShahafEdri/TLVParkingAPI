import logging
import os
import sys
from datetime import datetime

LOGGING_DIR = 'logs'

logger = logging.getLogger('prk-logger')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
streamHandler = logging.StreamHandler(stream=sys.stdout)
streamHandler.setLevel(logging.INFO)
# create formatter
FORMAT1 = '[%(asctime)s] %(levelname)-9s in %(filename)s: %(message)s'
FORMAT2 = '[%(asctime)s] %(filename)-20s %(levelname)s: %(message)s'
formatter = logging.Formatter(FORMAT2.ljust(40))
# add formatter to ch
streamHandler.setFormatter(formatter)
# add ch to logger
logger.addHandler(streamHandler)
# Add file handler + UUID for PD runs
timestamp = str(datetime.now()).replace(" ", "_")
timestamp = str(datetime.strftime(datetime.now(), '%Y_%m_%d_%H_%M_%S'))
# check if log dir exists
if not os.path.exists(LOGGING_DIR):
    os.makedirs(LOGGING_DIR)
fileHandler = logging.FileHandler(f"{LOGGING_DIR}/{logger.name}__{timestamp}.log", mode="w")
fileHandler.set_name("file-handler")
fileHandler.setFormatter(formatter)
fileHandler.setLevel(logging.DEBUG)
logger.addHandler(fileHandler)
# Don't allow root loggers to propagate so logging is not multiplied
logger.propagate = False
logger.info(f"INTRO: Will save log to: <{fileHandler.baseFilename}>")

logger.info("INTRO: Logger initialized")

if __name__ == "__main__":
    logger.info("INTRO: This is a test")
    logger.debug("INTRO: This is a test")
    logger.warning("INTRO: This is a test")
    logger.error("INTRO: This is a test")
    logger.critical("INTRO: This is a test")
