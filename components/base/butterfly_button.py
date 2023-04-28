from PyQt5.QtCore import QPointF, pyqtSignal
from PyQt5.QtGui import QPainter, QPainterPath, QColor, QPixmap
from PyQt5.QtWidgets import QLabel

from ...constants import BUTTERFLY_BUTTON_STATE

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
    update_state_signal = pyqtSignal(int)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def __init__(self, state=BUTTERFLY_BUTTON_STATE.CLOSE):
        super().__init__()
        self._state = state
        self.update_state_signal.connect(self._update_state)

        # self.layout = QVBoxLayout()
        # self.setLayout(self.layout)
        self.setObjectName("butterfly_button")
        # self.setStyleSheet(style_container)

        # self._colors = {
        #     True: QColor(0, 255, 60),
        #     False: QColor(255, 0, 0)
        # }
        self._pictures = {
            # True: "../../../assets/butterfly_button/green_valve.png",
            # True: "grapheneqtui/assets/butterfly_button/green_valve.png",
            # False: "../../assets/butterfly_button/red_valve.png",
            # False: "grapheneqtui/assets/butterfly_button/red_valve.png",
            BUTTERFLY_BUTTON_STATE.INACTIVE: "grapheneqtui/assets/butterfly_button/gray_valve.png",
            BUTTERFLY_BUTTON_STATE.OPEN: "grapheneqtui/assets/butterfly_button/green_valve.png",
            BUTTERFLY_BUTTON_STATE.CLOSE: "grapheneqtui/assets/butterfly_button/red_valve.png",
            BUTTERFLY_BUTTON_STATE.REGULATION: "grapheneqtui/assets/butterfly_button/yellow_valve.png",
        }
        # self._active = False

        # pixmap = QPixmap(self._pictures[self._state])
        # self.setPixmap(pixmap)
        # self.update_active(self._active)
        self._update_state(self._state)
        # Optional, resize window to image size
        # self.resize(pixmap.width(), pixmap.height())

        # self.clicked.connect(self.on_click)
        # self.setContentsMargins(0, 0, 0, 0)
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

    # def on_click(self):
    #     # print("On click butterfly!!!", self._active)
    #     self._active = not self._active
    #     self.update_ui()

    # def update_active(self, is_active):
    #     self._active = is_active
    #     # print("On click butterfly::", self._active)
    #     self.update_ui()

    def _update_state(self, state):
        self._state = state
        self.update_ui()

    def update_ui(self):
        try:
            pixmap = QPixmap(self._pictures[self._state])
            self.setPixmap(pixmap)
            # Optional, resize window to image size
            self.resize(pixmap.width(), pixmap.height())
            # print("PIXMAP!!!!", pixmap.width(), pixmap.height())
            # self.resize(200, 100)
        except Exception as e:
            print("Show picture butterfly error", e)
