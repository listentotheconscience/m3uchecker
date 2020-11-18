import tkinter as tk
from helpers import from_rgb


class EntryLine:
    def __init__(self, master):
        self.width = 20
        self.name = tk.Entry(master, width=self.width)
        self.group = tk.Entry(master, width=self.width)
        self.url = tk.Entry(master, width=self.width)

    def place(self, x: list, y: int):
        self.name.place(x=x[0], y=y)
        self.group.place(x=x[1], y=y)
        self.url.place(x=x[2], y=y)

    def grid(self, row):
        self.name.grid(row=row, column=0, sticky=tk.W + tk.E)
        self.group.grid(row=row, column=1, sticky=tk.W + tk.E)
        self.url.grid(row=row, column=2, sticky=tk.W + tk.E)

    def get_name(self):
        return self.name.get()

    def get_group(self):
        return self.group.get()

    def get_url(self):
        return self.url.get()

    def remove(self):
        self.name.grid_forget()
        self.group.grid_forget()
        self.url.grid_forget()

    def config(self, bg, fg):
        self.name.config(bg=from_rgb(bg))
        self.group.config(bg=from_rgb(bg))
        self.url.config(bg=from_rgb(bg))

        self.name.config(fg=from_rgb(fg))
        self.group.config(fg=from_rgb(fg))
        self.url.config(fg=from_rgb(fg))

    def setDisabled(self):
        self.name.config(bg=from_rgb((207, 102, 121)))
        self.group.config(bg=from_rgb((207, 102, 121)))
        self.url.config(bg=from_rgb((207, 102, 121)))

    def setEnabled(self):
        self.name.config(bg=from_rgb((3, 218, 198)))
        self.group.config(bg=from_rgb((3, 218, 198)))
        self.url.config(bg=from_rgb((3, 218, 198)))
        # self.name.config(fg=from_rgb((255, 255, 255)))
        # self.group.config(fg=from_rgb((255, 255, 255)))
        # self.url.config(fg=from_rgb((255, 255, 255)))
