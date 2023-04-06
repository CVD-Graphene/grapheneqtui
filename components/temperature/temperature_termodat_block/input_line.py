from PyQt5 import QtCore
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QLineEdit, QLabel, QHBoxLayout
from .styles import styles


class TemperatureInputLine(QWidget):
    def __init__(self,
                 label_1="T =",
                 label_2="°C",
                 input_validator_args=None,
                 parent=None):
        super().__init__(parent=parent)

        if input_validator_args is None:
            input_validator_args = [0, 1000, 2]

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.input_container)

        self.label_1 = QLabel()
        self.label_1.setText(label_1)
        self.label_1.setStyleSheet(styles.label)

        self.label_2 = QLabel()
        self.label_2.setText(label_2)
        self.label_2.setStyleSheet(styles.label)

        self.input = QLineEdit()
        self.input.setStyleSheet(styles.input)
        self.input.setValidator(QDoubleValidator(*input_validator_args))

        self.layout.addWidget(self.label_1, stretch=1, alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(self.input, stretch=3)
        self.layout.addWidget(self.label_2, 1)