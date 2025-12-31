from logging import Formatter, StreamHandler, getLogger

LOG_FORMAT = "%(asctime)s - %(levelname)s - %(name)s:%(lineno)d - %(message)s"

class Logger:
    def __init__(self, name: str, level: str = "INFO"):
        self.logger = getLogger(name)
        self.logger.setLevel(level)

        handler = StreamHandler()
        handler.setFormatter(Formatter(LOG_FORMAT))
        handler.setLevel(level)

        self.logger.addHandler(handler)
        self.logger.propagate = False

    def get_logger(self):
        return self.logger