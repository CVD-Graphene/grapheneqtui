from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QHBoxLayout, QVBoxLayout, QLabel
from ..utils import StyleSheet

SIDE = 2000

styles = StyleSheet({
    "container": {
        "name": "QWidget#main_block_widget",
        # "width": "100%",
        # "background-color": "rgb(220, 220, 255)",
    },
    "inactive_widget": {
        "name": "QWidget#inactive_widget",
        "width": f'{SIDE}px',
        "min-width": f'{SIDE}px',
        'height': f'{SIDE}px',
        'min-height': f'{SIDE}px',
        # 'opacity': '0.5',
        'background-color': "rgba(200, 200, 200, 0.2)",
    },
    "label_step_name": {
        # "height": "50px",
        # "min-width": f'300px',
        'background-color': "rgba(200, 200, 10, 0.8)",
        'font-size': "24px",
    }
})

CURRENT_STEP_START_NAME = "ТЕКУЩЕЕ     » "
PREVIOUS_STEP_START_NAME = "ВЫПОЛНЕННОЕ » "


class BaseMainBlockWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent=parent)

        self.layout = QHBoxLayout()
        self.setLayout(self.layout)
        self.setObjectName("main_block_widget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet("* {background-color: rgb(0, 0, 255);}")

        self.set_layout_content()

        self.inactive_widget = QWidget(parent=self)
        self.inactive_widget.setObjectName("inactive_widget")
        self.inactive_widget.setStyleSheet(styles.inactive_widget)
        self.inactive_widget.hide()

        self.recipe_labels_layout = QVBoxLayout()

        self.last_recipe_step = QLabel()
        self.last_recipe_step.setStyleSheet(styles.label_step_name)

        self.current_recipe_step = QLabel()
        self.current_recipe_step.setStyleSheet(styles.label_step_name)

        self.current_recipe_status = QLabel()
        self.current_recipe_status.setStyleSheet(styles.label_step_name)

        self.recipe_labels_layout.addWidget(
            self.current_recipe_status, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, stretch=1)
        self.recipe_labels_layout.addWidget(
            self.current_recipe_step, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, stretch=1)
        self.recipe_labels_layout.addWidget(
            self.last_recipe_step, alignment=QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft, stretch=1)
        self.recipe_labels_layout.addWidget(
            QLabel(), stretch=100)

        self.current_recipe_step_text = ""
        self.last_recipe_step_text = ""
        self.current_recipe_status_text = ""

        self.inactive_widget.setLayout(self.recipe_labels_layout)

    def set_layout_content(self):
        pass

    def deactivate_interface(self):
        self.inactive_widget.show()

    def activate_interface(self):
        self.current_recipe_step_text = ""
        self.last_recipe_step_text = ""
        self.current_recipe_step_text = ""
        self.current_recipe_step.setText(self.current_recipe_step_text)
        self.current_recipe_status.setText(self.current_recipe_status_text)
        self.last_recipe_step.setText(self.last_recipe_step_text)

        self.inactive_widget.hide()

    def set_current_step(self, step=""):
        self.last_recipe_step_text = PREVIOUS_STEP_START_NAME + \
                                     self.current_recipe_step_text[len(CURRENT_STEP_START_NAME):]
        self.current_recipe_step_text = CURRENT_STEP_START_NAME + step

        self.current_recipe_step.setText(self.current_recipe_step_text)
        self.last_recipe_step.setText(self.last_recipe_step_text)

    def set_current_recipe_status(self, status):
        self.current_recipe_status_text = "Текущий статус выполнения: " + status
        self.current_recipe_status.setText(self.current_recipe_status_text)
