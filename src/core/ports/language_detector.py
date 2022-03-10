from abc import ABC, abstractmethod

class LanguageDetectorPort(ABC):

    @abstractmethod
    def detect(self):
        ...
