from widgets import Window


class ScreenProperties:
    def __init__(self, master: Window):
        self.screenWidth = master.getInstance().winfo_screenmmwidth()
        self.screenHeight = master.getInstance().winfo_screenmmheight()

        self.middlePoint = [self.screenWidth // 2, self.screenHeight //2]
        self._windowSize = {}

    def setWindowSize(self, width, height):
        self._windowSize['width'] = width
        self._windowSize['height'] = height

    def getWindowSize(self):
        return self._windowSize
