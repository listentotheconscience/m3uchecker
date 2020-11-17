import tkinter as tk
from tkinter import ttk
from tkinter.filedialog import askopenfilename, asksaveasfilename
from EntryLine import EntryLine
from M3UParser import M3UParser
from EntryLineContainer import EntryLineContainer
from Channel import Channel
from ChannelContainer import ChannelContainer
from urllib import request
from helpers import from_rgb
from widgets import Button, Label, Window, Entry


class Tool:

    def __init__(self):
        self.root = Window()
        self.root.title("M3U Checker")
        self.root.style(from_rgb((21, 21, 21)))
        self.root.resizable(False)

        self.screen_w = self.root.getInstance().winfo_screenmmwidth()
        self.screen_h = self.root.getInstance().winfo_screenmmheight()
        self.middle_point = [self.screen_w // 2, self.screen_h // 2]

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
        self.filename = askopenfilename(filetypes=[("M3U Playlist", "*.m3u"), ("All Files", "*.*")])
        self.parser = M3UParser(self.filename)

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

    def _fillEntry(self, entry: EntryLine, data: dict):
        entry.name.insert(0, data['name'])
        entry.group.insert(0, data['group'])
        entry.url.insert(0, data['url'])

        return entry

    def _createEntry(self, increment=False):
        el = EntryLine(self.scrollable_frame)
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
            request.urlopen(address, timeout=1)
            return True
        except Exception:
            return False

    def _pingChannels(self):
        channel = 0
        for item in self.channelContainer.container():
            result = self._ping(item.getUrl())
            if result is False:
                self.container.getItem(channel).setDisabled()
            else:
                self.container.getItem(channel).setEnabled()
            channel += 1

    def _addEntry(self):
        self._createEntry(True)

    def _removeEntry(self):
        self.container.removeLast()

    def _checkURLWindow(self):
        newWindow = Window(main=False, master=self.root.getInstance())
        newWindow.style(from_rgb((21, 21, 21)))
        newWindow.title("Check URL")
        newWindow.resizable(False)
        newWindow.geometry([200, 80], self.middle_point)

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
        window_size = [500, 720]
        self.root.geometry(window_size, self.middle_point)

        # Make Scrollable frame
        style = ttk.Style()
        style.configure("A.TFrame", background=from_rgb((30, 30, 30)))

        container = ttk.Frame(self.root.getInstance(), width=370, height=460, borderwidth=0, relief=tk.FLAT, style="A.TFrame")
        canvas = tk.Canvas(container, width=370, height=460, borderwidth=0, relief=tk.FLAT)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview,
                                  style="Custom.Vertical.TScrollbar")
        self.scrollable_frame = ttk.Frame(canvas, borderwidth=0, relief=tk.FLAT, style="A.TFrame")

        container.config()
        canvas.config()
        scrollbar.config()
        self.scrollable_frame.config()

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(
                scrollregion=canvas.bbox("all")
            )
        )

        canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        canvas.configure(yscrollcommand=scrollbar.set)
        container.place(x=30, y=35)
        canvas.grid(sticky=tk.NSEW)
        scrollbar.grid(row=0, column=3, sticky=tk.N + tk.S + tk.E)

        canvas.config(bg=from_rgb((30, 30, 30)))

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
