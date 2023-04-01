from abc import ABC, abstractmethod


class Create(ABC):
    @abstractmethod
    def create(self, objeto):
        pass

class Update(ABC):
    @abstractmethod
    def update(self, data, id):
        pass

class Delete(ABC):
    @abstractmethod
    def delete(self, id):
        pass

class Read(ABC):
    @abstractmethod
    def find_one(self, objeto):
        pass