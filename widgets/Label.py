import tkinter as tk
from .Widget import Widget


class Label(Widget):
    def __init__(self, master):
        self._label = tk.Label(master)
        super().__init__(self._label)

    def style(self, bg, fg, **kwargs):
        self.config(bg=bg, fg=fg, **kwargs)
        return self

    def command(self, func):
        pass

    def getInstance(self):
        return self._label