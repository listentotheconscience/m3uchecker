from dataStructures import Channel
from dataStructures import Container


class ChannelContainer(Container):

    def __init__(self):
        self._container = []
        super().__init__(self._container)

    def append(self, instance: Channel):
        for item in self._container:
            if instance.getUrl() == item.getUrl():
                return
            if instance.getName() == item.getName() and (instance.getGroup() != item.getGroup() or instance.getUrl() != item.getUrl()):
                self._container.remove(item)
                break

        self._container.append(instance)

    def searchByName(self, name) -> Channel:
        for item in self.container():
            if name == item.getName():
                return item

    def searchByUrl(self, url) -> Channel:
        for item in self.container():
            if url == item.getUrl():
                return item

    def searchByGroup(self, group) -> list:
        output = []
        for item in self.container():
            if group == item.getGroup():
                output.append(item)
        return output

    def update(self, instance: Channel, data: dict):
        if instance in self.container():
            instance.name = data['name']
            instance.group = data['group']
            instance.url = data['url']

