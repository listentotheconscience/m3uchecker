import tkinter as tk
from tkinter import ttk


class ScrollableFrame:
    def __init__(self, master):
        # style = ttk.Style()
        # style.configure("A.TFrame", background=from_rgb((30, 30, 30)))

        # w=370 h=460 r=FLAT

        self.container = ttk.Frame(master)
        self.canvas = tk.Canvas(self.container)
        self.scrollbar = ttk.Scrollbar(self.container, orient="vertical", command=self.canvas.yview)

        self.scrollable_frame = ttk.Frame(self.canvas)

        self.container.config()
        self.canvas.config()
        self.scrollbar.config()
        self.scrollable_frame.config()

        self.scrollable_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all")
            )
        )

        self.canvas.create_window((0, 0), window=self.scrollable_frame, anchor="nw")

        self.canvas.configure(yscrollcommand=self.scrollbar.set)

        # canvas.config(bg=from_rgb((30, 30, 30)))

    def canvasStyle(self, bg, **kwargs):
        self.canvas.config(bg=bg, **kwargs)
        return self

    def containerStyle(self, bg, **kwargs):
        style = ttk.Style()
        style.configure("A.TFrame", background=bg, **kwargs)
        self.container.config(style="A.TFrame")
        return self

    def placeContainer(self, x, y, **kwargs):
        self.container.place(x=x, y=y, **kwargs)
        return self

    def placeCanvas(self, x, y, **kwargs):
        self.canvas.place(x=x, y=y, **kwargs)
        return self

    def placeScrollbar(self, x, y, **kwargs):
        self.scrollbar.place(x=x, y=y, **kwargs)
        return self

    def gridContainer(self, row=None, column=None, sticky=None, **kwargs):
        self.container.grid(row=row, column=column, sticky=sticky, **kwargs)
        return self

    def gridCanvas(self, row=None, column=None, sticky=None, **kwargs):
        self.canvas.grid(row=row, column=column, sticky=sticky, **kwargs)
        return self

    def gridScrollbar(self, row=None, column=None, sticky=None, **kwargs):
        self.scrollbar.grid(row=row, column=column, sticky=sticky, **kwargs)
        return self

    def canvasConfig(self, **kwargs):
        self.canvas.config(**kwargs)
        return self

    def containerConfig(self, **kwargs):
        self.container.config(**kwargs)
        return self

    def scrollbarConfig(self, **kwargs):
        self.scrollbar.config(**kwargs)
        return self

    def style(self, bg, **kwargs):
        style = ttk.Style()
        style.configure("B.TFrame", background=bg, **kwargs)
        self.scrollable_frame.config(style="B.TFrame")

    def config(self, **kwargs):
        self.scrollable_frame.config(**kwargs)
        return self

    def getInstance(self):
        return self.scrollable_frame