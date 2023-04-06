from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QHBoxLayout

button_style = """
QPushButton#button_valve_control {
    height: 90px;
    width: 90px;
    border-radius: 45px;
    background-color: rgb(254, 100, 100);
    border-style: solid;
    border-width: 1px;
    border-color: rgba(0,0,100,255);
}
QPushButton#button_valve_control:pressed {
    background-color: rgb(155, 100, 100);
}
"""


class PumpButton(QPushButton):
    def __init__(self):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("button_valve_control")
        self.setStyleSheet(button_style)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # self.button = QPushButton()
        # self.button.setObjectName("button_valve_control")
        # self.button.setStyleSheet(button_style)
        # self.w = ValveLines()
        # self.layout.addWidget(self.w)
