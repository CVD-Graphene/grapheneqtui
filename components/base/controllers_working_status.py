from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QDoubleValidator
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QHBoxLayout, QLabel

from .latex_widget import LatexWidget
from ...constants import COLORS
from ...utils import StyleSheet

styles = StyleSheet({
    "container": {
        # "name": "QWidget#controllers_working_status_widget",
        # "min-width": "20px",
        "max-width": "20px",
        "width": "20px",
        #
        # "min-height": '20px',
        # "max-height": '20px',
        # "height": '20px',
        # "border-radius": "5px",
        "border-radius": "10px",
        # "background-color": COLORS.LIGHT_GREEN,
        # "background-color": "rgb(0, 255, 0)",
    },
    "label": {
        "name": "QLabel#label_controllers_working_status_widget",
        "min-width": "20px",
        # "max-width": "20px",
        # "width": "20px",

        # "min-height": '20px',
        # "max-height": '20px',
        "height": '20px',
        "border-radius": "10px",
        "background-color": COLORS.LIGHT_GREEN,
        # "background-color": "rgb(0, 255, 0)",
    },
    "incorrect": {
        "background-color": "rgba(255, 0, 0, 0)",
    },
})


class ControllersWorkingStatusWidget(QWidget):
    update_working_status_signal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        # self.layout.setContentsMargins(10, 10, 10, 10)
        self.setStyleSheet(styles.container)
        self.setObjectName("controllers_working_status_widget")
        self.update_working_status_signal.connect(self._update_working_status)

        self.label = QLabel(' ')
        self.label.setObjectName("label_controllers_working_status_widget")
        self.label.setStyleSheet(styles.label)
        self.layout.addWidget(self.label, alignment=QtCore.Qt.AlignCenter)

    def _update_working_status(self, value: bool):
        if value:
            self.label.setStyleSheet(styles.label)
        else:
            self.label.setStyleSheet(styles.union('label', 'incorrect'))
