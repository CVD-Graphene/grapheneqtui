from PyQt5.QtCore import pyqtSignal
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtWidgets import QVBoxLayout
from ...utils import StyleSheet

WIDTH = "300px"

styles = StyleSheet({
    "container": {
        "max-height": "60px",
        "min-height": "60px",
        "min-width": WIDTH,
        "width": WIDTH,

        "max-width": WIDTH,
        # "width": '100%',
        "background-color": "rgb(200, 200, 200)",
        # "border-style": "solid",
        "border-radius": "4px",
        "padding-left": "8px",
        "font-size": "28px",
        "text-align": "center",
    },
})


class LatexWidget(QtWidgets.QWidget):
    update_text_color_signal = pyqtSignal(str)

    def __init__(self,
                 text="$F_2$",
                 parent=None,
                 rgb=None,
                 fon_size_mult=1.5,
                 text_color="#000000",
                 top_y=0.9,
                 ):
        super().__init__(parent)
        self.text_color = text_color
        self.text = text
        if rgb is None:
            self.rgb = [200, 200, 200]
        else:
            self.rgb = rgb
        self.fon_size_mult = fon_size_mult
        self.top_y = top_y

        l = QVBoxLayout(self)
        l.setContentsMargins(0, 0, 0, 0)

        r, g, b, a = self.palette().base().color().getRgbF()
        facecolor = (self.rgb[0] / 255, self.rgb[1] / 255, self.rgb[2] / 255)
        self._figure = Figure(edgecolor=(r, g, b), facecolor=facecolor)
        self._canvas = FigureCanvas(self._figure)
        # self._canvas.siz
        l.addWidget(self._canvas)
        self._update_ui()

        self.update_text_color_signal.connect(self._update_text_color)

    def _update_text_color(self, text_color):
        if text_color != self.text_color:
            self.text_color = text_color
            self._update_ui()

    def _setText(self, mathText):
        if self.text != mathText:
            self.text = mathText
            self._update_ui()
        # self.setStyleSheet(styles.container)
        # l = QVBoxLayout(self)
        # l.setContentsMargins(0, 0, 0, 0)

        # r, g, b, a = self.palette().base().color().getRgbF()
        # facecolor = (self.rgb[0]/255, self.rgb[1]/255, self.rgb[2]/255)
        # self._figure = Figure(edgecolor=(r, g, b), facecolor=facecolor)
        # self._canvas = FigureCanvas(self._figure)
        # # self._canvas.siz
        # l.addWidget(self._canvas)
        # self._figure.clear()

    def _update_ui(self):
        text = self._figure.suptitle(
            self.text,
            x=0.09,
            y=self.top_y,
            horizontalalignment='left',
            verticalalignment='top',
            size=QtGui.QFont().pointSize() * self.fon_size_mult,
            color=self.text_color,
        )
        # self._canvas.draw()

        (x0, y0), (x1, y1) = text.get_window_extent().get_points()
        w = x1 - x0
        h = y1 - y0

        self._figure.set_size_inches(w / 80, h / 80)
        self.setFixedSize(w, h * 1.05)
        self._canvas.draw()
        # self._figure.show()

    def setText(self, mathText):
        # self.__init__(mathText=mathText)
        self._setText(mathText)
