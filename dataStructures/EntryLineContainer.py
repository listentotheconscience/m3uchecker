from widgets import EntryLine
from dataStructures import Container


class EntryLineContainer(Container):
    def __init__(self):
        self._container = []
        super().__init__(self._container)

    def append(self, data: EntryLine):
        if not isinstance(data, EntryLine):
            raise TypeError("Data must be EntryLine type")
        self._container.append(data)


    def toList(self):
        return [[item.get_name(), item.get_group(), item.get_url()] for item in self._container]

    def removeLast(self):
        self.container().pop().remove()
        self._container.pop()

    def clear(self):
        for item in self.container():
            item.remove()
        self.container().clear()