from PyQt5.QtCore import pyqtSignal

from grapheneqtui.components import ParameterLatexLabel
from ...utils import StyleSheet

styles = StyleSheet({
    "container": {
        "max-height": "60px",
        # "max-width": "200px",
        # "width": '100%',
        "background-color": "rgb(200, 200, 200)",
        # "border-style": "solid",
        "border-radius": "8px",
        # "border-width": "1px",
        # "border-color": "rgba(0,0,100,255)",
        "padding-left": "8px",
        "font-size": "24px",
        "text-align": "center",
    },
})


class ShowPressureBlock(ParameterLatexLabel):
    update_pressure_signal = pyqtSignal(float)

    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.update_pressure_signal.connect(self._set_value)
        self._set_value(0.0)

        # shadow = QGraphicsDropShadowEffect()
        # # setting blur radius
        # shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # # adding shadow to the label
        # self.setGraphicsEffect(shadow)

    def set_value(self, value):
        print("DEPRECATED Remove set_value from ShowPressureBlock!")
        self._set_value(value)

    def _set_value(self, value):
        self.value = str(round(value, 1))
        self.setText(f"P = ${value}$ mbar")
