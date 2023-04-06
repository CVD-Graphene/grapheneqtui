from PyQt5.QtWidgets import QTableWidgetItem, QLineEdit, QDoubleSpinBox, QSpinBox


class TableItem(object):
    def __init__(self, widget):
        self.widget = widget
        # if isinstance(self.widget, QTableWidgetItem):
        #     w = QTableWidgetItem()
        #     w.s
        #     widget.

    @property
    def is_item(self):
        if isinstance(self.widget, QTableWidgetItem):
            return True
        return False


TIME_MINUTES_DIGITS_MAX = 4
TIME_SECONDS_DIGITS_MAX = 2


class AppQTimeEdit(QLineEdit):
    def __init__(self, parent=None, text="0:00"):
        super().__init__(parent=parent)
        self.setInputMask(f"{'0' * TIME_MINUTES_DIGITS_MAX}:{'0' * TIME_SECONDS_DIGITS_MAX}")
        self.setText(text)
        # self.textChanged.connect(self._on_change)

    def setText(self, a0: str) -> None:
        m, s = '0', '0'
        try:
            m, s = list(map(str, map(int, a0.strip().split(':'))))
        except:
            pass
        text = f"{m.zfill(TIME_MINUTES_DIGITS_MAX)}:{s.zfill(TIME_SECONDS_DIGITS_MAX)}"
        super().setText(text)

    # def _on_change(self):
    #     self.setText(self.text())


class AppQSpinBox(QSpinBox):
    def __init__(self, parent=None, maximum=1000000):
        super().__init__(parent=parent)
        self.setMaximum(maximum)


class AppQDoubleSpinBox(QDoubleSpinBox):
    def __init__(self, parent=None, maximum=10000000, decimals=6):
        super().__init__(parent=parent)
        self.setMaximum(maximum)
        self.setDecimals(decimals)
