from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QLabel, QVBoxLayout, QGraphicsDropShadowEffect

from .latex_widget import LatexWidget
from ...constants import SHADOW_BLUR_RADIUS
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
        # "border-width": "1px",
        # "border-color": "rgba(0,0,100,255)",
        "padding-left": "8px",
        "font-size": "28px",
        "text-align": "center",
    },
})

# cl = LatexWidget
cl = QLabel


class ParameterLatexLabel(QWidget):
    def __init__(self,
                 parent=None,
                 # rgb=(200, 200, 200),
                 ):
        super().__init__(parent=parent)

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        self.math = LatexWidget("", parent=self)
        self.layout.addWidget(self.math, alignment=QtCore.Qt.AlignCenter)

        # self.setAlignment(QtCore.Qt.AlignCenter)

        # self.setText("P = 1,3 * 10000 mbar")
        self.setText("")
        shadow = QGraphicsDropShadowEffect()
        # setting blur radius
        shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # adding shadow to the label
        self.setGraphicsEffect(shadow)

    def setText(self, text):
        # self.math.hide()
        self.math.setText(text)
        # self.math.update()
        # self.math = LatexWidget(text, parent=self)
        # self.layout.addWidget(self.math, alignment=QtCore.Qt.AlignCenter)
        # self.layout.addWidget(self.math, alignment=QtCore.Qt.AlignCenter)
        # self.math.show()
