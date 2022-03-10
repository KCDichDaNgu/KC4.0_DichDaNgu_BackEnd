from abc import ABC, abstractmethod

class ContentTranslatorPort(ABC):

    @abstractmethod
    def translate(self):
        ...
