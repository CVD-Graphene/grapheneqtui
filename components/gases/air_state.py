from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QLabel

from ...components import ButterflyButton
from .styles import styles
from ...constants import BUTTERFLY_BUTTON_STATE


class AirStateWidget(QWidget):
    on_update_is_valve_open_signal = pyqtSignal(bool)
    update_is_valve_open_signal = pyqtSignal()
    confirmation_press_time_ms = 5000

    def __init__(self):
        super().__init__()

        self.is_waiting = False
        self.state = BUTTERFLY_BUTTON_STATE.CLOSE
        self.timer = QTimer(parent=None)

        self.line = QWidget(self)
        self.line.setStyleSheet(styles.line)
        self.line.setFixedWidth(self.width() - 120)
        self.line.move(120, 80)  # -self.height() // 2

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.air_container)
        self.setObjectName("air_state_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.gas = QLabel()
        self.gas.setText("Air")
        self.gas.setStyleSheet(styles.gas)
        self.gas.setAlignment(QtCore.Qt.AlignCenter)

        self.b = ButterflyButton()

        self.label = QLabel()
        self.label.setText(f"1 bar")
        self.label.setStyleSheet(styles.down_label)
        self.label.setAlignment(QtCore.Qt.AlignCenter)

        self.layout.addWidget(self.gas, stretch=1, alignment=QtCore.Qt.AlignLeft)
        self.layout.addWidget(self.label, stretch=1, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.b, stretch=4, alignment=QtCore.Qt.AlignHCenter,)

        self.on_update_is_valve_open_signal.connect(self._draw_is_open)
        self.b.clicked.connect(self._on_click_butterfly)

    def _draw_is_open(self, is_open: bool):
        self.is_waiting = False
        self.state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
        self.b.update_state_signal.emit(self.state)

    def _on_click_butterfly(self):
        if self.is_waiting or self.state == BUTTERFLY_BUTTON_STATE.OPEN:
            self.update_is_valve_open_signal.emit()
            self.is_waiting = False
        else:
            self.is_waiting = True
            self.b.update_state_signal.emit(BUTTERFLY_BUTTON_STATE.REGULATION)
            self.timer.singleShot(
                self.confirmation_press_time_ms,
                self._clear_button_waiting
            )

    def _clear_button_waiting(self):
        if self.state == BUTTERFLY_BUTTON_STATE.OPEN:
            return
        self.is_waiting = False
        self._draw_is_open(False)

    # def draw_is_open(self, is_open):
    #     state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
    #     self.b.update_state_signal.emit(state)
    #     # self.b.update_active(is_open)
    #
    # def connect_valve_function(self, func):
    #     def on_click():
    #         ans = func()
    #         if type(ans) in [bool, int]:
    #             self.draw_is_open(ans)
    #
    #     self.b.clicked.connect(on_click)
