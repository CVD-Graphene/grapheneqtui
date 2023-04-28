from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QLabel

from ...constants import PUMP_BUTTON_STATE


class PumpButton(QLabel):
    clicked = pyqtSignal()
    update_state_signal = pyqtSignal(int)

    def mousePressEvent(self, ev):
        self.clicked.emit()

    def __init__(self, state=PUMP_BUTTON_STATE.CLOSE):
        super().__init__()
        self._state = state
        self.update_state_signal.connect(self._update_state)

        self.setObjectName("pump_button")

        self._pictures = {
            PUMP_BUTTON_STATE.INACTIVE: "grapheneqtui/assets/pump_button/gray_pump.png",
            PUMP_BUTTON_STATE.OPEN: "grapheneqtui/assets/pump_button/green_pump.png",
            PUMP_BUTTON_STATE.CLOSE: "grapheneqtui/assets/pump_button/red_pump.png",
        }
        self._update_state(self._state)

    def _update_state(self, state):
        self._state = state
        self.update_ui()

    def update_ui(self):
        try:
            pixmap = QPixmap(self._pictures.get(self._state))
            self.setPixmap(pixmap)
            # Optional, resize window to image size
            self.resize(pixmap.width(), pixmap.height())
        except Exception as e:
            print("Show picture pump button error", e)
