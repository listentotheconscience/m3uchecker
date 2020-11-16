class Channel:
    def __init__(self, name, group, url):
        self.name = name
        self.group = group
        self.url = url

    def getName(self):
        return self.name

    def getGroup(self):
        return self.group

    def getUrl(self):
        return self.url

    def getM3ULine(self):
        return f'#EXTINF:-1 group-title="{self.getGroup()}", {self.getName()}\n{self.getUrl()}\n'

    def toDict(self):
        return {
            'name': self.getName(),
            'group': self.getGroup(),
            'url': self.getUrl()
        }

