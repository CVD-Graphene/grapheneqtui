from PyQt5 import QtCore
from PyQt5.QtWidgets import QWidget, QVBoxLayout

from ..components import GasStateWidget, AirStateWidget
from ..utils import StyleSheet

styles = StyleSheet({
    "container": {
        "name": "QWidget#pressure_block",
        "min-width": "250px",
        "max-width": "600px",
        # "width": "100%",
        # "height": '100%',
        # "background-color": "rgb(140, 240, 210)",
        "border-right-style": "solid",
        "border-right-width": "2px",
        "border-right-color": "#000000",
    },
})


class BaseValvesControlBlock(QWidget):
    def __init__(self,
                 parent=None,
                 gases_configuration=None,
                 default_sccm_value=200.0,
                 ):
        super().__init__(parent=parent)

        self.gases_configuration = gases_configuration
        self.default_sccm_value = default_sccm_value

        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.layout.setContentsMargins(14, 14, 2, 14)
        self.setObjectName("pressure_block")
        self.setStyleSheet(styles.container)
        self.setContentsMargins(0, 0, 0, 0)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        self.set_control_valves()
        self.set_air_valve()

        self.gases = []
        self.set_gases_valves()

    def set_control_valves(self):
        pass

    def set_air_valve(self):
        self.air = AirStateWidget()
        self.layout.addWidget(self.air)

    def set_gases_valves(self):
        for i, valve_config in enumerate(self.gases_configuration):
            gas = valve_config['NAME']
            max_sccm = valve_config.get('MAX_SCCM', self.default_sccm_value)
            gas_widget = GasStateWidget(gas=gas, number=i, max_sccm=max_sccm)
            setattr(self, gas, gas_widget)

            gas_attr = getattr(self, gas)
            self.layout.addWidget(gas_attr)
            self.gases.append(gas_attr)

    def draw_set_gas_target_sccm(self, sccm, gas_num):
        # self.gases[gas_num].draw_set_target_sccm(sccm)
        self.gases[gas_num].column_info.update_target_signal.emit(sccm)

    def draw_is_open_gas(self, is_open, gas_num):
        # self.gases[gas_num].draw_is_open(is_open)
        self.gases[gas_num].on_update_is_valve_open_signal.emit(is_open)

    def draw_is_open_air(self, is_open):
        self.air.draw_is_open(is_open)
