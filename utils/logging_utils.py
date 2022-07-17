from logging import WARNING, Formatter, basicConfig, getLogger, INFO, FileHandler, StreamHandler


FORMAT = '[%(asctime)s] %(levelname)s in %(filename)s: %(message)s'
# file handler
file_handler = FileHandler('server_REST.log', mode='a',)
file_handler.setLevel(WARNING)
file_handler.setFormatter(Formatter(FORMAT))
# stream handler
stream_handler = StreamHandler()
stream_handler.setLevel(INFO)
stream_handler.setFormatter(Formatter(FORMAT))
# logger
logger = getLogger()
logger.addHandler(file_handler)
logger.addHandler(stream_handler)

