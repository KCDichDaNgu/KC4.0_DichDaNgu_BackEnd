from abc import ABC, abstractmethod
from typing import Optional, Any

class BackgroundTaskManagerPort(ABC):

    @abstractmethod
    def start(self):
        ...
    
    @abstractmethod
    def stop(self):
        ...
    
    @abstractmethod
    def add_job(self):
        ...
