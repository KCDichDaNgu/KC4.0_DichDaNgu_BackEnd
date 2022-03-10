from abc import ABC, abstractmethod
from typing import Optional, Any

class LoggerPort(ABC):

    @abstractmethod
    def log(self):
        ...
    
    @abstractmethod
    def error(self):
        ...
    
    @abstractmethod
    def warn(self):
        ...

    @abstractmethod
    def debug(self):
        ...
