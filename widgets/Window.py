import tkinter as tk


class Window:
    def __init__(self, main=True, master=None):
        if main is True:
            self.window = tk.Tk(master)
        else:
            self.window = tk.Toplevel(master)

    def geometry(self, winsize: list, offset: list):
        self.window.geometry(f'{winsize[0]}x{winsize[1]}+{offset[0]}+{offset[1]}')
        return self

    def title(self, title: str):
        self.window.title(title)
        return self

    def overrideredirect(self, value):
        self.window.overrideredirect = value
        return self

    def resizable(self, value):
        if isinstance(value, list):
            self.window.resizable(width=value[0], height=value[1])
        else:
            self.window.resizable(width=value, height=value)
        return self

    def config(self, **kwargs):
        self.window.config(**kwargs)
        return self

    def style(self, bg=None, fg=None, **kwargs):
        self.config(bg=bg, fg=fg, **kwargs)
        return self

    def getInstance(self):
        return self.window
