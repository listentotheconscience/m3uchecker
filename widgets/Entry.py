import tkinter as tk
from .Widget import Widget


class Entry(Widget):
    def __init__(self, master):
        self._entry = tk.Entry(master)
        super().__init__(self._entry)

    def style(self, bg, fg, **kwargs):
        self.config(bg=bg, fg=fg, **kwargs)
        return self

    def command(self, func):
        pass

    def getInstance(self):
        return self._entry
