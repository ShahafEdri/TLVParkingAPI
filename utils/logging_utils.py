import logging
import sys
from datetime import datetime

logger = logging.getLogger('prk-logger')
logger.setLevel(logging.DEBUG)
# create console handler and set level to debug
ch = logging.StreamHandler(stream=sys.stdout)
ch.setLevel(logging.INFO)
# create formatter
formatter = logging.Formatter('[%(asctime)s] %(levelname)-9s: %(filename)s - %(message)s'.ljust(40))
# add formatter to ch
ch.setFormatter(formatter)
# add ch to logger
logger.addHandler(ch)
# Add file handler + UUID for PD runs
timestamp = str(datetime.now()).replace(" ", "_")
timestamp = str(datetime.strftime(datetime.now(), '%Y_%m_%d_%H_%M_%S'))
fileHandler = logging.FileHandler(f"{logger.name}__{timestamp}.log", mode="w")
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
