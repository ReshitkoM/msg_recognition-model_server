from abc import ABC, abstractmethod

class ModelBase(ABC):

    @abstractmethod
    def predict(self, data):
        pass