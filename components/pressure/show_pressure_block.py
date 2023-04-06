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
    def __init__(self, parent=None):
        super().__init__(parent=parent)
        self.set_value("0.0")

        # shadow = QGraphicsDropShadowEffect()
        # # setting blur radius
        # shadow.setBlurRadius(SHADOW_BLUR_RADIUS)
        # # adding shadow to the label
        # self.setGraphicsEffect(shadow)

    def set_value(self, value):
        self.value = str(value)
        self.setText(f"P = ${value}$ mbar")
