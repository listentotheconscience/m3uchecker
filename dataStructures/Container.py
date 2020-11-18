from abc import abstractmethod


class Container:

    def __init__(self, instance):
        self.instance = instance

    @abstractmethod
    def append(self, instance):
        pass

    def pop(self):
        return self.instance[-1]

    def container(self):
        return self.instance

    def getItem(self, index):
        return self.instance[index]
