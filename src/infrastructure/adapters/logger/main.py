import logging
from core.ports import LoggerPort

class Logger(LoggerPort):

    def __init__(self, name) -> None:
        super().__init__()

        self.__logger = logging.getLogger(name)
        self.__name = name

    @property
    def name(self):
        return self.__name

    @property
    def log(self):
        return self.__logger.log
    
    @property
    def error(self):
        return self.__logger.error
    
    @property
    def warn(self):
        return self.__logger.warn

    @property
    def debug(self):
        return self.__logger.debug
