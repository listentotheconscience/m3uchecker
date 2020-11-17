import tkinter as tk
from .Widget import Widget


class Button(Widget):
    def __init__(self, master):
        self._button = tk.Button(master)
        super().__init__(self._button)

    def style(self, bg, fg, **kwargs):
        self.config(bg=bg, fg=fg, **kwargs)
        return self

    def command(self, func):
        self.config(command=func)
        return self

    def getInstance(self):
        return self._button