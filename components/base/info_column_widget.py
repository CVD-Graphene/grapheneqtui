from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel

from .latex_widget import LatexWidget
from ...utils import StyleSheet

styles = StyleSheet({
    # "container": {
    #     "name": "QWidget#gas_state_widget",
    #     "max-height": "120px",
    #     # "max-width": "5000px",
    #     # "width": "100%",
    #     # "height": '100%',
    #     # "background-color": "rgb(0, 240, 0)",
    # },
    "up_label": {
        "max-height": "60px",
        "width": '100%',
        # "margin-left": "10px",
        # "min-width": "180px",
        # "width": "120px",
        "background-color": "rgba(255, 255, 0, 0)",
        # "background-color": "rgb(255, 255, 255)",
        "font-size": "28px",
    },
    "down_label": {
        "max-height": "60px",
        "min-width": "180px",
        # "width": "120px",
        "background-color": "rgb(180, 180, 180)",
        "font-size": "28px",
    },
    "input": {
        "font-size": "28px",
        # "height:": "100%",
        "max-height": "60px",
        # "min-width": "50px",
        "background-color": "rgba(210, 210, 210, 0)",
        # "border-color": "rgba(210, 210, 210, 0)",
        "border": "none",
        # "background-color": LIGHT_GREEN,
        # "width": "90%",
        # "max-width": "100px",
    }
})


class InfoColumnWidget(QWidget):
    update_current_signal = pyqtSignal(float)
    update_target_signal = pyqtSignal(float)
    on_update_target_signal = pyqtSignal(float)
    down_latex_fon_size_mult = 1.3

    def __init__(self,
                 max_value=200.0,
                 min_value=0.0,
                 decimals=1,
                 unit="sccm"):
        super().__init__()
        self.unit = unit
        self.max_value = max_value
        self.min_value = min_value
        self.decimals = decimals

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # self.layout.setContentsMargins(0, 0, 0, 0)
        # self.setStyleSheet(styles.container)
        # self.setObjectName("gas_state_widget")
        # self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.input = QLineEdit()
        self.input.setStyleSheet(styles.input)
        # self.input.setMinimumWidth(1000)
        if self.max_value:
            self.input.setValidator(QDoubleValidator(
                self.min_value, self.max_value, self.decimals))

        self.input.setText(f"{self.min_value}")
        self.input.setInputMethodHints(Qt.ImhFormattedNumbersOnly)

        self.up_label = QLabel()
        self.up_label.setText(self.unit)
        self.up_label.setStyleSheet(styles.up_label)
        self.up_label.setAlignment(QtCore.Qt.AlignCenter)

        self.up_widget = QHBoxLayout()
        self.up_widget.addWidget(self.input, stretch=1, alignment=QtCore.Qt.AlignLeft)
        self.up_widget.addWidget(self.up_label, stretch=1, alignment=QtCore.Qt.AlignRight)

        # self.down_label = QLabel()
        self.down_label = LatexWidget(
            fon_size_mult=self.down_latex_fon_size_mult,
        )
        self.down_label.setText(f"{self.min_value} {self.unit}")
        self.down_label.setStyleSheet(styles.down_label)
        # self.down_label.setAlignment(QtCore.Qt.AlignCenter)

        # self.info_layout_widget = QWidget()
        # self.info_layout_widget.setStyleSheet("background-color: #000000;max-height: 200px;")
        # self.info_layout = QVBoxLayout()
        # self.info_layout_widget.setLayout(self.info_layout)
        self.layout.addLayout(self.up_widget)
        # self.info_layout.addWidget(self.up_widget, alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(self.down_label, alignment=QtCore.Qt.AlignTop)

        self.layout.setSpacing(0)
        # self.layout.setSpacing(0)

        self.update_current_signal.connect(self._update_current_value_label)
        self.update_target_signal.connect(self._update_target_value_label)
        self.input.returnPressed.connect(self._on_update_input_value)

    def _update_current_value_label(self, value: float):
        # print("NEW VALUE CURRENT SCCM DRAW:", value)
        self.down_label.setText(self.get_label_text_format(value))

    def get_label_text_format(self, value: float):
        return f"${round(value, self.decimals)}$ {self.unit}"

    def _update_target_value_label(self, value: float):
        self.input.setText(f"{round(value, self.decimals)}")

    def _on_update_input_value(self):
        input_value = self.input.text().replace(',', '.')
        value = float(input_value)
        # print("! INPUT TARGET VALUE:", value)
        self.on_update_target_signal.emit(value)
