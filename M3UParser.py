import re
import pathlib

class M3UParser:

    def __init__(self, filename):
        self.filename = filename
        self.channels = []
        self.strings = []

        self.patterns = {
            'name': r",\s*[a-zA-Zа-яёА-ЯЁ0-9 ]+",
            'group': r'group-title="\s*[a-zA-Zа-яёА-ЯЁ ]+"',
            'url': r"(https?|ftp)://[^\s/$.?#].[^\s]*"
        }

        with open(self.filename, encoding='utf-8-sig' ,mode='r') as f:
            for line in f:
                if line.strip() is not '':
                    self.strings.append(line.strip())
            self.strings = self.strings[1:]

        self._fill()
        del self.strings

    def _getName(self, string):
        try:
            return re.search(self.patterns['name'], string).group().replace(',', '').strip()
        except Exception:
            return ""

    def _getGroup(self, string):
        try:
            return re.search(self.patterns['group'], string).group().split('"')[1].strip()
        except Exception:
            return ""

    def _getUrl(self, string):
        try:
            return re.search(self.patterns['url'], string).group().strip()
        except Exception:
            return ""

    def _fill(self):
        item = 0
        while item in range(len(self.strings) - 1):
            name = self._getName(self.strings[item])
            group = self._getGroup(self.strings[item])
            url = self._getUrl(self.strings[item + 1])
            self.channels.append({
                'name': name,
                'group': group,
                'url': url
            })

            item += 2

if __name__ == '__main__':
    parser = M3UParser(r"A:\IPTV\NadTV.m3u")

    print(parser.channels)