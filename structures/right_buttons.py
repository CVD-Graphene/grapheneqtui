from PyQt5 import QtCore
from PyQt5.QtWidgets import QPushButton, QWidget, QGridLayout, QVBoxLayout

from ..components import ControllersWorkingStatusWidget
from ..constants import LIGHT_GREEN
from ..utils import StyleSheet


styles = StyleSheet({
    "container": {
        # "name": "QWidget",
        "max-width": "240px",
        "min-width": "180px",
        # "background-color": "rgb(150, 250, 250)",
    },
    "close_button": {
        "name": "QPushButton#button_close",
        "height": "70px",
        "font-size": "20px",
        "background-color": "rgb(255, 150, 150)",
    },
    "settings_button": {
        "name": "QPushButton#settings_button",
        "height": "70px",
        "font-size": "20px",
        "background-color": "rgb(255, 255, 230)",
    },
    "run_recipe_button": {
        "name": "QPushButton#run_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": LIGHT_GREEN,
    },
    "edit_recipe_button": {
        "name": "QPushButton#edit_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": LIGHT_GREEN,
    },
    "pause_recipe_button": {
        "name": "QPushButton#pause_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": 'rgb(255, 255, 0)',
    },
    "stop_recipe_button": {
        "name": "QPushButton#stop_recipe_button",
        "min-height": "100px",
        "padding": "10px",
        "font-size": "24px",
        "background-color": 'rgb(255, 0, 0)',
    },
})


class RightButtonsWidget(QWidget):
    def __init__(self,
                 on_close=None,
                 on_create_recipe=None,
                 on_open_recipe=None,
                 on_pause_recipe=None,
                 on_stop_recipe=None,
                 on_get_recipe_state=None,
                 recipe_states=None,
                 ):
        super().__init__()
        self.on_pause_recipe = on_pause_recipe
        self.on_get_recipe_state = on_get_recipe_state

        self.recipe_states = recipe_states
        assert self.recipe_states is not None

        self.layout = QGridLayout()
        self.setLayout(self.layout)
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)
        # self.setStyleSheet("background-color: rgb(0, 0, 255);")

        self.button_close = QPushButton("CLOSE X")
        self.button_close.setObjectName("button_close")
        self.button_close.clicked.connect(on_close)
        self.button_close.setStyleSheet(styles.close_button)

        self.system_status_widget = ControllersWorkingStatusWidget()

        self.button_settings = QPushButton("SETTINGS")
        self.button_settings.setObjectName("settings_button")
        self.button_settings.setStyleSheet(styles.settings_button)

        self.select_recipe = QPushButton("Select and\nrun recipe")
        self.select_recipe.setObjectName("run_recipe_button")
        self.select_recipe.clicked.connect(on_open_recipe)
        self.select_recipe.setStyleSheet(styles.run_recipe_button)

        # self.select_recipe = QPushButton("Create\nrecipe")
        # self.select_recipe.setObjectName("run_recipe_button")
        # self.select_recipe.setStyleSheet(styles.run_recipe_button)

        self.edit_recipe = QPushButton("Create\nrecipe")
        self.edit_recipe.setObjectName("edit_recipe_button")
        self.edit_recipe.clicked.connect(on_create_recipe)
        self.edit_recipe.setStyleSheet(styles.edit_recipe_button)

        self.layout.addWidget(self.button_close, 0, 0, alignment=QtCore.Qt.AlignTop)
        self.layout.addWidget(self.system_status_widget, 1, 0,
                              # alignment=QtCore.Qt.AlignTop
                              )
        # self.right_buttons_layout.setRowMinimumHeight(0, 10)
        # self.right_buttons_layout.setRowStretch(0, 10)

        self.layout.addWidget(self.button_settings, 2, 0, QtCore.Qt.AlignTop)
        self.layout.setRowMinimumHeight(1, 100)
        # self.right_buttons_layout.setRowStretch(1, 1)

        self.pause_recipe = QPushButton("▋▋/▶")
        self.is_pause = False
        self._update_pause_button()
        self.pause_recipe.setObjectName("pause_recipe_button")
        self.pause_recipe.clicked.connect(self._on_pause)
        self.pause_recipe.setStyleSheet(styles.pause_recipe_button)

        self.stop_recipe = QPushButton("STOP")
        self.stop_recipe.setObjectName("stop_recipe_button")
        if on_stop_recipe:
            self.stop_recipe.clicked.connect(on_stop_recipe)
        self.stop_recipe.setStyleSheet(styles.stop_recipe_button)

        self.layout.addWidget(self.select_recipe, 3, 0)
        self.layout.addWidget(self.edit_recipe, 4, 0)

        self.layout.addWidget(self.pause_recipe, 5, 0)
        self.layout.addWidget(self.stop_recipe, 6, 0)

        self.stop_recipe.hide()
        self.pause_recipe.hide()

    def _update_pause_button(self):
        # pass
        self.pause_recipe.setText("RUN" if self.is_pause else "PAUSE")

    def _on_pause(self):
        if self.on_pause_recipe:
            # print("## ON PAUSE CLICKED!")
            self.on_pause_recipe()
            current_state = self.on_get_recipe_state()
            self.is_pause = current_state == self.recipe_states.PAUSE
            # print(f"%% ON PAUSE INFO: state: {current_state}, is_pause: {self.is_pause}")
            self._update_pause_button()

    def activate_manage_recipe_buttons(self):
        self.select_recipe.hide()
        self.button_settings.hide()
        self.edit_recipe.hide()

        self.pause_recipe.show()
        self.stop_recipe.show()

    def deactivate_manage_recipe_buttons(self):
        self.select_recipe.show()
        self.button_settings.show()
        self.edit_recipe.show()

        self.pause_recipe.hide()
        self.stop_recipe.hide()
