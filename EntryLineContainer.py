from EntryLine import EntryLine
from Container import Container


class EntryLineContainer(Container):
    def __init__(self):
        self._container = []

    def append(self, data: EntryLine):
        if not isinstance(data, EntryLine):
            raise TypeError("Data must be EntryLine type")
        self._container.append(data)

    def pop(self):
        return self._container[-1]

    def toList(self):
        return [[item.get_name(), item.get_group(), item.get_url()] for item in self._container]

    def container(self):
        return self._container

    def getItem(self, index):
        return self._container[index]

    def removeLast(self):
        self.container().pop().remove()
        self._container.pop()
