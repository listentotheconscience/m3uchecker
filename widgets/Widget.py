import tkinter as tk
from abc import abstractmethod


class Widget:

    def __init__(self, instance):
        self._instance = instance

    def config(self, **kwargs):
        self._instance.config(**kwargs)
        return self

    def place(self, x, y, **kwargs):
        self._instance.place(x=x, y=y, **kwargs)

    def grid(self, row, column, **kwargs):
        self._instance.grid(**kwargs)

    def pack(self, **kwargs):
        self._instance.pack(**kwargs)

    @abstractmethod
    def style(self, bg, fg, **kwargs):
        pass

    @abstractmethod
    def command(self, func):
        pass

    @abstractmethod
    def getInstance(self):
        pass