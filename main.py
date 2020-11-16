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

class Tool:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("M3U Checker")
        self.root.config(bg=from_rgb((21,21,21)))
        # self.root.overrideredirect(True)
        self.root.resizable(width=False, height=False)
        self.scrollable_frame = None
        self.screen_w = self.root.winfo_screenmmwidth()
        self.screen_h = self.root.winfo_screenmmheight()
        self.middle_point = [self.screen_w // 2, self.screen_h // 2]
        self.window_size = [500, 720]
        self.row = -1

        self.URLlabel = None
        self.URLentry = None

        self.channels = 0
        self.container = EntryLineContainer()
        self.channelContainer = ChannelContainer()
        self.filename = None
        self.parser = None

    def _openfile(self):
        self.filename = askopenfilename(parent=self.root, filetypes=[("M3U Playlist", "*.m3u"), ("All Files", "*.*")])
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
        newWindow = tk.Toplevel(self.root)
        newWindow.config(bg=from_rgb((21, 21, 21)))
        newWindow.title("Check URL")
        # newWindow.overrideredirect(True)
        newWindow.resizable(width=False, height=False)
        # closeProgramButton = tk.Button(newWindow, text='X', justify=tk.CENTER, command=newWindow.destroy, relief=tk.FLAT)
        # closeProgramButton.config(bg=from_rgb((30, 30, 30)))
        # closeProgramButton.config(fg=from_rgb((255, 255, 255)))

        newWindow.geometry(f"200x80+{self.middle_point[0]}+{self.middle_point[1]}")
        self.URLlabel = tk.Label(newWindow, text="Channel Status: ")
        self.URLlabel.config(bg=from_rgb((21, 21, 21)), fg=from_rgb((255, 255, 255)))
        self.URLentry = tk.Entry(newWindow,)
        self.URLlabel.config(bg=from_rgb((30, 30, 30)), fg=from_rgb((255, 255, 255)))
        button = tk.Button(newWindow,text="Check", justify=tk.CENTER, command=self._checkURL, borderwidth=0, relief=tk.FLAT)
        button.config(bg=from_rgb((30, 30, 30)), fg=from_rgb((255, 255, 255)))
        self.URLlabel.pack(side=tk.TOP)
        self.URLentry.pack(side=tk.TOP)
        button.pack(side=tk.TOP)
        # closeProgramButton.place(x=180, y=0)

    def _checkURL(self):
        text = self.URLentry.get()
        result = self._ping(text)
        if result == True:
            self.URLlabel['text'] = "Channel Status: Enabled"
        else:
            self.URLlabel['text'] = "Channel Status: Disabled"

    def create_window(self):
        # Set Window props
        self.root.geometry(f'{self.window_size[0]}x{self.window_size[1]}+{self.middle_point[0]}+{self.middle_point[1]}')

        #Make Scrollable frame
        style = ttk.Style()
        style.configure("A.TFrame", background=from_rgb((30, 30, 30)))
        scrollbarStyle = ttk.Style()
        scrollbarStyle.configure("Custom.Vertical.TScrollbar", gripcount=0,
                                 background=from_rgb((30, 30, 30)), darkcolor=from_rgb((48, 48, 48)),
                                 lightcolor=from_rgb((66, 66, 66)), troughcolor=from_rgb((48, 48, 48)),
                                 bordercolor=from_rgb((48,48,48)), arrowcolor=from_rgb((66, 66, 66)))

        container = ttk.Frame(self.root, width=370, height=460, borderwidth=0, relief=tk.FLAT, style="A.TFrame")
        canvas = tk.Canvas(container, width=370, height=460, borderwidth=0, relief=tk.FLAT)
        scrollbar = ttk.Scrollbar(container, orient="vertical", command=canvas.yview, style="Custom.Vertical.TScrollbar")
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
        nameLabel = tk.Label(text='Name', justify=tk.CENTER)
        groupLabel = tk.Label(text='Group', justify=tk.CENTER)
        urlLabel = tk.Label(text='Url', justify=tk.CENTER)

        nameLabel.config(bg=from_rgb((21, 21, 21)))
        groupLabel.config(bg=from_rgb((21, 21, 21)))
        urlLabel.config(bg=from_rgb((21, 21, 21)))

        nameLabel.config(fg=from_rgb((255, 255, 255)))
        groupLabel.config(fg=from_rgb((255, 255, 255)))
        urlLabel.config(fg=from_rgb((255, 255, 255)))

        nameLabel.place(x=70, y=10)
        groupLabel.place(x=70 + 120, y=10)
        urlLabel.place(x=70 + (120 * 2), y=10)

        # Buttons
        openFileButton = tk.Button(text='Open File', justify=tk.CENTER, command=self._openfile, borderwidth=1, relief=tk.FLAT)
        saveFileButton = tk.Button(text='Save File', justify=tk.CENTER, command=self._savefile, borderwidth=1, relief=tk.FLAT)
        pingChannelButton = tk.Button(text='Check Channels', justify=tk.CENTER, command=self._pingChannels, borderwidth=1, relief=tk.FLAT)
        addEntryButton = tk.Button(text='+', justify=tk.CENTER, command=self._addEntry, borderwidth=1, relief=tk.FLAT)
        removeEntryButton = tk.Button(text='-', justify=tk.CENTER, command=self._removeEntry, borderwidth=1, relief=tk.FLAT)
        checkChannelButton = tk.Button(text='Ping URL', justify=tk.CENTER, command=self._checkURLWindow, borderwidth=1, relief=tk.FLAT)
        # closeProgramButton = tk.Button(text='X', justify=tk.CENTER, command=self.root.destroy, relief=tk.FLAT)

        openFileButton.config(bg=from_rgb((30, 30, 30)))
        saveFileButton.config(bg=from_rgb((30, 30, 30)))
        pingChannelButton.config(bg=from_rgb((30, 30, 30)))
        addEntryButton.config(bg=from_rgb((30, 30, 30)))
        removeEntryButton.config(bg=from_rgb((30, 30, 30)))
        checkChannelButton.config(bg=from_rgb((30, 30, 30)))
        # closeProgramButton.config(bg=from_rgb((30, 30, 30)))

        openFileButton.config(fg=from_rgb((255, 255, 255)))
        saveFileButton.config(fg=from_rgb((255, 255, 255)))
        pingChannelButton.config(fg=from_rgb((255, 255, 255)))
        addEntryButton.config(fg=from_rgb((255, 255, 255)))
        removeEntryButton.config(fg=from_rgb((255, 255, 255)))
        checkChannelButton.config(fg=from_rgb((255, 255, 255)))
        # closeProgramButton.config(fg=from_rgb((255, 255, 255)))

        openFileButton.place(x=30, y=670)
        saveFileButton.place(x=95, y=670)
        pingChannelButton.place(x=170, y=670)
        addEntryButton.place(x=370, y=510)
        removeEntryButton.place(x=390, y=510)
        checkChannelButton.place(x=270, y=670)
        # closeProgramButton.place(x=480, y=0)





    def loop(self):
        self.root.mainloop()


if __name__ == '__main__':
    app = Tool()
    app.create_window()
    app.loop()
