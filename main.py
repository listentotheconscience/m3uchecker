import socket
import time
import tkinter as tk
import threading
import urllib.request
import urllib.error
from tkinter.filedialog import askopenfilename, asksaveasfilename
from dataStructures import EntryLineContainer, ChannelContainer, Channel, M3UParser, ScreenProperties
from helpers import from_rgb
from widgets import Button, Label, Window, Entry, EntryLine, ScrollableFrame


class Tool:

    def __init__(self):
        self.root = Window()
        self.root.title("M3U Checker")
        self.root.style(from_rgb((21, 21, 21)))
        self.root.resizable(False)

        self.screenProperties = ScreenProperties(self.root)

        self.scrollable_frame = None
        self.row = -1

        self.URLLabel = None
        self.URLEntry = None

        self.channels = 0
        self.container = EntryLineContainer()
        self.channelContainer = ChannelContainer()
        self.filename = None
        self.parser = None

    def _openfile(self):
        self.channelContainer.container().clear()
        self._clearEntries()
        self.container.clear()
        self.filename = askopenfilename(filetypes=[("M3U Playlist", "*.m3u"), ("All Files", "*.*")])
        self.parser = M3UParser(self.filename)

        self.root.title(f"M3U Checker: [{self.filename.split('/')[-1]}]")

        self._parseFile()

    def _savefile(self):
        filename = asksaveasfilename(filetypes=[("M3U Playlist", "*.m3u"), ("All Files", "*.*")])
        string = "#EXTM3U\n"
        for item in self.container.container():
            channel = self.channelContainer.searchByName(item.get_name())
            data = {
                'name': item.get_name(),
                'group': item.get_group(),
                'url': item.get_url(),
            }
            self.channelContainer.update(channel, data)
            channel = self.channelContainer.searchByName(item.get_name())
            string += channel.getM3ULine()

        with open(filename, encoding='utf-8-sig', mode='w') as f:
            f.write(string)

    def _clearEntries(self):
        for entry in self.container.container():
            entry.name.delete(0, tk.END)
            entry.group.delete(0, tk.END)
            entry.url.delete(0, tk.END)
            entry.config((66, 66, 66), (255, 255, 255))

    def _fillEntry(self, entry: EntryLine, data: dict):
        entry.name.insert(0, data['name'])
        entry.group.insert(0, data['group'])
        entry.url.insert(0, data['url'])

        return entry

    def _createEntry(self, increment=False):
        el = EntryLine(self.scrollable_frame.getInstance())
        el.config((66, 66, 66), (255, 255, 255))
        self.row += 1
        el.grid(self.row)
        self.container.append(el)
        if increment:
            self.channels += 1

    def _createEntries(self, channels):
        for i in range(channels):
            self._createEntry()

    def _parseFile(self):
        self.channels = len(self.parser.channels)
        self._createEntries(self.channels)
        ch = 0
        for item in self.parser.channels:
            channel = Channel(item['name'], item['group'], item['url'])
            self.channelContainer.append(channel)
            self._fillEntry(self.container.getItem(ch), channel.toDict())
            ch += 1

    def _ping(self, address):
        try:
            urllib.request.urlopen(address, timeout=0.5)
            return True
        except urllib.error.URLError:
            return False

    def _pingChannels(self):
        def ping():
            i = 0
            for item in self.channelContainer.container():
                try:
                    try:
                        urllib.request.urlopen(item.getUrl(), timeout=0.5)
                    except socket.timeout:
                        time.sleep(1)
                        urllib.request.urlopen(item.getUrl(), timeout=0.5)
                    self.container.getItem(i).setEnabled()
                except urllib.error.URLError:
                    self.container.getItem(i).setDisabled()
                i += 1

        thread = threading.Thread(target=ping)
        thread.daemon = True
        thread.start()


    def _addEntry(self):
        self._createEntry(True)

    def _removeEntry(self):
        self.container.removeLast()

    def _checkURLWindow(self):
        self.screenProperties.setWindowSize(200, 80)
        newWindow = Window(main=False, master=self.root.getInstance())
        newWindow.style(from_rgb((21, 21, 21)))
        newWindow.title("Check URL")
        newWindow.resizable(False)
        newWindow.geometry(self.screenProperties.getWindowSize(), self.screenProperties.middlePoint)

        self.URLLabel = Label(newWindow.getInstance()).config(text='Channel Status')
        self.URLLabel.style(from_rgb((21, 21, 21)), from_rgb((255, 255, 255)))

        self.URLEntry = Entry(newWindow.getInstance())
        self.URLEntry.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)))

        button = Button(newWindow.getInstance()).config(text='Check', justify=tk.CENTER).command(self._checkURL)
        button.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)

        self.URLLabel.pack(side=tk.TOP)
        self.URLEntry.pack(side=tk.TOP)
        button.pack(side=tk.TOP)

    def _checkURL(self):
        text = self.URLEntry.getInstance().get()
        result = self._ping(text)
        if result is True:
            self.URLLabel.config(text="Channel Status: Enabled")
        else:
            self.URLLabel.config(text="Channel Status: Disabled")

    def createWindow(self):
        # Set Window props
        self.screenProperties.setWindowSize(500, 720)
        self.root.geometry(self.screenProperties.getWindowSize(), self.screenProperties.middlePoint)

        # Make Scrollable frame

        self.scrollable_frame = ScrollableFrame(self.root.getInstance())
        self.scrollable_frame.canvasStyle(from_rgb((30, 30, 30))).containerStyle(from_rgb((30, 30, 30)))
        self.scrollable_frame.containerConfig(width=370, height=460, relief=tk.FLAT).canvasConfig(width=370, height=460, relief=tk.FLAT)
        self.scrollable_frame.config(relief=tk.FLAT).style(from_rgb((30, 30, 30)))
        self.scrollable_frame.placeContainer(30, 35).gridCanvas(sticky=tk.NSEW).gridScrollbar(0, 3, tk.N + tk.S + tk.E)

        # Labels
        nameLabel = Label(self.root.getInstance()).config(text='Name', justify=tk.CENTER)
        groupLabel = Label(self.root.getInstance()).config(text='Group', justify=tk.CENTER)
        urlLabel = Label(self.root.getInstance()).config(text='URL', justify=tk.CENTER)

        nameLabel.style(from_rgb((21, 21, 21)), from_rgb((255, 255, 255)))
        groupLabel.style(from_rgb((21, 21, 21)), from_rgb((255, 255, 255)))
        urlLabel.style(from_rgb((21, 21, 21)), from_rgb((255, 255, 255)))

        nameLabel.place(x=70, y=10)
        groupLabel.place(x=70 + 120, y=10)
        urlLabel.place(x=70 + (120 * 2), y=10)

        # Buttons
        openFileButton = Button(self.root.getInstance()).config(text='Open File', justify=tk.CENTER).command(self._openfile)
        saveFileButton = Button(self.root.getInstance()).config(text='Save File', justify=tk.CENTER).command(self._savefile)
        pingChannelButton = Button(self.root.getInstance()).config(text='Ping Channels', justify=tk.CENTER).command(self._pingChannels)
        addEntryButton = Button(self.root.getInstance()).config(text='+', justify=tk.CENTER).command(self._addEntry)
        removeEntryButton = Button(self.root.getInstance()).config(text='-', justify=tk.CENTER).command(self._removeEntry)
        checkChannelButton = Button(self.root.getInstance()).config(text='Ping URL', justify=tk.CENTER).command(self._checkURLWindow)

        openFileButton.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)
        saveFileButton.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)
        pingChannelButton.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)
        addEntryButton.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)
        removeEntryButton.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)
        checkChannelButton.style(from_rgb((30, 30, 30)), from_rgb((255, 255, 255)), relief=tk.FLAT)

        openFileButton.place(x=30, y=670)
        saveFileButton.place(x=95, y=670)
        pingChannelButton.place(x=170, y=670)
        addEntryButton.place(x=370, y=510)
        removeEntryButton.place(x=390, y=510)
        checkChannelButton.place(x=270, y=670)

    def loop(self):
        self.root.getInstance().mainloop()


if __name__ == '__main__':
    app = Tool()
    app.createWindow()
    app.loop()
