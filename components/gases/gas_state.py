from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, QTimer
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel

from .. import InfoColumnWidget
from ...components import ButterflyButton, LatexWidget
from .styles import styles
from ...constants import BUTTERFLY_BUTTON_STATE


class GasStateWidget(QWidget):
    update_target_sccm_signal = pyqtSignal(float, int)
    on_update_is_valve_open_signal = pyqtSignal(bool)
    update_is_valve_open_signal = pyqtSignal(int)
    on_update_gas_name_color_by_pressure_signal = pyqtSignal(int)

    def __init__(self,
                 gas="O2",
                 number=None,
                 max_sccm=200.0,
                 unit="sccm"):
        super().__init__()

        self.gas_name = gas
        self.number = number
        self.max_sccm = max_sccm
        self._on_system_change_sccm = None
        self.unit = unit

        # LINE !
        # self.line = QWidget(self)
        # self.line.setStyleSheet(styles.line)
        # self.line.setFixedWidth(self.width() - 120)
        # # print("HEIGHT!!!", self.height() // 2) # 240 = h/2 ????
        # self.line.move(120, 60)  # -self.height() // 2

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        self.setStyleSheet(styles.container)
        self.setObjectName("gas_state_widget")
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # self.line = QLineEdit()
        # self.layout.addWidget(self.line)

        # self.gas = QLabel()
        # self.gas = ParameterLatexLabel()
        self.gas = LatexWidget(
            text=f"${gas}$",
            rgb=[240, 240, 240],
            fon_size_mult=2.0
        )
        # self.gas.setText(gas)
        self.gas.setStyleSheet(styles.gas)
        # self.gas.setAlignment(QtCore.Qt.AlignCenter)

        self.b = ButterflyButton()
        self.column_info = InfoColumnWidget(
            max_value=self.max_sccm,
            min_value=0.0,
            unit="sccm",
        )

        # self.input = QLineEdit()
        # self.input.setStyleSheet(styles.input)
        # # self.input.setMinimumWidth(1000)
        # self.input.setValidator(QDoubleValidator(0.0, self.max_sccm, 1))
        # self.input.setText("0")
        # self.input.returnPressed.connect(self.on_update_input_sccm)
        #
        # self.up_label = QLabel()
        # self.up_label.setText(f"sccm")
        # self.up_label.setStyleSheet(styles.up_label)
        # self.up_label.setAlignment(QtCore.Qt.AlignCenter)
        #
        # self.up_widget = QHBoxLayout()
        # self.up_widget.addWidget(self.input, stretch=1, alignment=QtCore.Qt.AlignLeft)
        # self.up_widget.addWidget(self.up_label, stretch=1, alignment=QtCore.Qt.AlignRight)
        #
        # self.down_label = QLabel()
        # self.down_label.setText(f"0 sccm")
        # self.down_label.setStyleSheet(styles.down_label)
        # self.down_label.setAlignment(QtCore.Qt.AlignCenter)
        #
        # self.info_layout_widget = QWidget()
        # # self.info_layout_widget.setStyleSheet("background-color: #000000;max-height: 200px;")
        # self.info_layout = QVBoxLayout()
        # self.info_layout_widget.setLayout(self.info_layout)
        # self.info_layout.addLayout(self.up_widget)
        # # self.info_layout.addWidget(self.up_widget, alignment=QtCore.Qt.AlignTop)
        # self.info_layout.addWidget(self.down_label, alignment=QtCore.Qt.AlignTop)
        #
        # self.info_layout.setSpacing(0)
        # self.layout.setSpacing(0)

        self.layout.addWidget(self.gas, stretch=1, alignment=QtCore.Qt.AlignLeft)
        # self.layout.addStretch(100)
        self.layout.addSpacing(50)
        # self.layout.addWidget(self.info_layout_widget, stretch=1, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.column_info, stretch=10, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.b, stretch=10, alignment=QtCore.Qt.AlignHCenter,)

        self.column_info.on_update_target_signal.connect(self._on_update_target_sccm)
        self.on_update_is_valve_open_signal.connect(self._draw_is_open)
        self.b.clicked.connect(self._on_click_butterfly)

        self.on_update_gas_name_color_by_pressure_signal.connect(self._draw_gas_name_color)

        self.tmp_timer = QTimer(parent=None)
        self.tmp_timer.singleShot(100, self._draw_gas_name_color)

    def _draw_gas_name_color(self, pressure=0.0):
        if pressure < 1.5:
            self.gas.update_text_color_signal.emit("#B00000")
        else:
            self.gas.update_text_color_signal.emit("#000000")

    def _on_update_target_sccm(self, sccm: float):
        self.update_target_sccm_signal.emit(sccm, self.number)

    # def update_current_sccm_label(self, value):
    #     # print("NEW VALUE CURRENT SCCM DRAW:", value)
    #     self.down_label.setText(f"{round(value, 1)} sccm")

    # def connect_change_sccm_function(self, func):
    #     self._on_system_change_sccm = func

    # def draw_is_open(self, is_open):
    #     # print("Draw is opened...", is_open, self.gas_name)
    #     # self.b._active = is_open
    #     state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
    #     self.b.update_state_signal.emit(state)
    #     # self.b.update_active(is_open)

    def _draw_is_open(self, is_open: bool):
        state = BUTTERFLY_BUTTON_STATE.OPEN if is_open else BUTTERFLY_BUTTON_STATE.CLOSE
        self.b.update_state_signal.emit(state)

    def _on_click_butterfly(self):
        self.update_is_valve_open_signal.emit(self.number)

    # def on_update_input_sccm(self):
    #     input_sccm = self.input.text()
    #     sccm = float(input_sccm)
    #     print("INPUT SCCM:", sccm)
    #     # if sccm > self.max_sccm:
    #     #     sccm = self.max_sccm
    #     #     self.draw_set_target_sccm(sccm)
    #     if self._on_system_change_sccm is not None:
    #         self._on_system_change_sccm(sccm, self.number)

    # def draw_set_target_sccm(self, sccm):
    #     self.input.setText(str(sccm))
