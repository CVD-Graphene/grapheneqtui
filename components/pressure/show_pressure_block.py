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

    def __init__(self, parent=None, digits_round=0):
        super().__init__(parent=parent)
        self.update_pressure_signal.connect(self._set_value)
        self._set_value(0.0)
        self.digits_round = digits_round

        # shadow = QGraphicsDropShadowEffect()
        # # setting blur radius
        # shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # # adding shadow to the label
        # self.setGraphicsEffect(shadow)

    def set_value(self, value):
        print("DEPRECATED Remove set_value from ShowPressureBlock!")
        self._set_value(value)

    def _set_value(self, value):
        self.value = value
        if self.value < 1:
            s = "{:.1E}".format(value).lower()
            num, degree = s.split('e')
            formatted_value = f"{num}*10^{{{int(degree)}}}"
        else:
            formatted_value = f"{round(self.value, self.digits_round)}"

        self.setText(f"P = ${formatted_value}$ mbar")
