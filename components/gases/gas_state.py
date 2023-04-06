from PyQt5 import QtCore
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel

from ...components import ButterflyButton, LatexWidget
from .styles import styles


class GasStateWidget(QWidget):
    def __init__(self, gas="O2", number=None, max_sccm=200.0):
        super().__init__()

        self.gas_name = gas
        self.number = number
        self.max_sccm = max_sccm
        self._on_system_change_sccm = None

        self.line = QWidget(self)
        self.line.setStyleSheet(styles.line)
        self.line.setFixedWidth(self.width() - 120)
        # print("HEIGHT!!!", self.height() // 2) # 240 = h/2 ????
        self.line.move(120, 60)  # -self.height() // 2
        # self.layout.addWidget(self.line, QtCore.Qt.AlignAbsolute)

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
            fon_size_mult=3.4
        )
        # self.gas.setText(gas)
        self.gas.setStyleSheet(styles.gas)
        # self.gas.setAlignment(QtCore.Qt.AlignCenter)

        self.b = ButterflyButton()

        self.input = QLineEdit()
        self.input.setStyleSheet(styles.input)
        # self.input.setMinimumWidth(1000)
        self.input.setValidator(QDoubleValidator(0.0, self.max_sccm, 1))
        self.input.setText("0")
        self.input.returnPressed.connect(self.on_update_input_sccm)

        self.up_label = QLabel()
        self.up_label.setText(f"sccm")
        self.up_label.setStyleSheet(styles.up_label)
        self.up_label.setAlignment(QtCore.Qt.AlignCenter)

        self.up_widget = QHBoxLayout()
        self.up_widget.addWidget(self.input, stretch=1, alignment=QtCore.Qt.AlignLeft)
        self.up_widget.addWidget(self.up_label, stretch=1, alignment=QtCore.Qt.AlignRight)

        self.down_label = QLabel()
        self.down_label.setText(f"0 sccm")
        self.down_label.setStyleSheet(styles.down_label)
        self.down_label.setAlignment(QtCore.Qt.AlignCenter)

        self.info_layout_widget = QWidget()
        # self.info_layout_widget.setStyleSheet("background-color: #000000;max-height: 200px;")
        self.info_layout = QVBoxLayout()
        self.info_layout_widget.setLayout(self.info_layout)
        self.info_layout.addLayout(self.up_widget)
        # self.info_layout.addWidget(self.up_widget, alignment=QtCore.Qt.AlignTop)
        self.info_layout.addWidget(self.down_label, alignment=QtCore.Qt.AlignTop)

        self.info_layout.setSpacing(0)
        # self.layout.setSpacing(0)

        self.layout.addWidget(self.gas, stretch=1, alignment=QtCore.Qt.AlignLeft)
        # self.layout.addStretch(10)
        self.layout.addWidget(self.info_layout_widget, stretch=1, alignment=QtCore.Qt.AlignCenter,)
        self.layout.addWidget(self.b, stretch=10, alignment=QtCore.Qt.AlignHCenter,)

    def update_current_sccm_label(self, value):
        # print("NEW VALUE CURRENT SCCM DRAW:", value)
        self.down_label.setText(f"{round(value, 1)} sccm")

    def connect_change_sccm_function(self, func):
        self._on_system_change_sccm = func

    def draw_is_open(self, is_open):
        # print("Draw is opened...", is_open, self.gas_name)
        # self.b._active = is_open
        self.b.update_active(is_open)

    def connect_valve_function(self, func):
        def on_click():
            ans = func(self.number)
            # print("GET ANS VALVE PRESS", ans)
            if type(ans) in [bool, int]:
                self.draw_is_open(ans)

        self.b.clicked.connect(on_click)

    def on_update_input_sccm(self):
        input_sccm = self.input.text()
        sccm = float(input_sccm)
        print("INPUT SCCM:", sccm)
        # if sccm > self.max_sccm:
        #     sccm = self.max_sccm
        #     self.draw_set_target_sccm(sccm)
        if self._on_system_change_sccm is not None:
            self._on_system_change_sccm(sccm, self.number)

    def draw_set_target_sccm(self, sccm):
        self.input.setText(str(sccm))
