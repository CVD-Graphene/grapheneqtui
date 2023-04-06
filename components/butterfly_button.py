from PyQt5.QtCore import QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPixmap
from PyQt5.QtWidgets import QLabel

# from .styles import styles

SIDE = 60
SIN_SIDE = 60 * (3 ** 0.5) / 2
"""
    height: 60px;
    min-height: 100px;
    min-width: 120px;
    width: 100%;
"""
style_container = """
QPushButton#butterfly_button {
    height: 60px;
    min-width: 120px;
    margin: 0;
    padding: 0;
    background-color: rgba(150, 255, 150, 0);
}
"""


class ButterflyButton(QLabel):
    clicked = pyqtSignal()

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def __init__(self):
        super().__init__()

        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setObjectName("butterfly_button")
        # self.setStyleSheet(style_container)

        self._colors = {
            True: QColor(0, 255, 60),
            False: QColor(255, 0, 0)
        }
        self._pictures = {
            # True: "../../../assets/butterfly_button/green_valve.png",
            True: "grapheneqtui/assets/butterfly_button/green_valve.png",
            # False: "../../assets/butterfly_button/red_valve.png",
            False: "grapheneqtui/assets/butterfly_button/red_valve.png",
            # False: "red_valve.png",
        }
        self._active = False

        pixmap = QPixmap(self._pictures[self._active])
        self.setPixmap(pixmap)
        self.update_active(self._active)
        # Optional, resize window to image size
        # self.resize(pixmap.width(), pixmap.height())

        # self.clicked.connect(self.on_click)
        # self.setContentsMargins(0, 0, 0, 0)
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    def on_click(self):
        # print("On click butterfly!!!", self._active)
        self._active = not self._active
        self.update_ui()

    def update_active(self, is_active):
        self._active = is_active
        # print("On click butterfly::", self._active)
        self.update_ui()

    def update_ui(self):
        try:
            pixmap = QPixmap(self._pictures[self._active])
            self.setPixmap(pixmap)
            # Optional, resize window to image size
            self.resize(pixmap.width(), pixmap.height())
            # print("PIXMAP!!!!", pixmap.width(), pixmap.height())
            # self.resize(200, 100)
        except Exception as e:
            print("Show picture butterfly error", e)

    def paintEvent1(self, event=None):
        try:
            qp = QPainter()
            qp.begin(self)

            # a = randint(10, 100)
            # d = a * math.tan(math.radians(30))
            x, y = 0, 0

            pos_tl = QPointF(x, y)
            pos_bl = QPointF(x, y + SIDE)
            pos_center = QPointF(x + SIN_SIDE, y + SIDE * 0.5)
            pos_center2 = QPointF(x + SIN_SIDE, y + SIDE * 0.5 + 1)
            pos_tr = QPointF(x + SIN_SIDE * 2, y)
            pos_br = QPointF(x + SIN_SIDE * 2, y + SIDE)

            qp.setBrush(self._colors[self._active])
            path = QPainterPath()
            path.moveTo(pos_tl)
            path.lineTo(pos_center)
            path.lineTo(pos_tr)
            path.lineTo(pos_br)
            path.lineTo(pos_center2)
            path.lineTo(pos_bl)
            path.lineTo(pos_tl)

            qp.drawPath(path)

            qp.end()
        except Exception as e:
            print("Draw triangle error", e)
