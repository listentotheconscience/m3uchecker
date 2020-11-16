from abc import abstractmethod


class Container:
    @abstractmethod
    def append(self, instance):
        pass

    @abstractmethod
    def pop(self):
        pass

    @abstractmethod
    def container(self):
        pass

    @abstractmethod
    def getItem(self, index):
        pass
