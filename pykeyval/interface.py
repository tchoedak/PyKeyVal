from abc import ABC, abstractmethod


class Store(ABC):
    @abstractmethod
    def get(self):
        pass

    @abstractmethod
    def set(self):
        pass

    @abstractmethod
    def delete(self):
        pass

    @abstractmethod
    def clear(self):
        pass
