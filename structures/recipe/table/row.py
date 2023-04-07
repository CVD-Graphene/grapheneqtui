from PyQt5.QtWidgets import QTableWidgetItem, QComboBox
from .cells import (
    TableItem, AppQSpinBox, AppQDoubleSpinBox, AppQTimeEdit,
)


class TableRow(object):

    def __init__(self, table, row_id, actions_list, items=None):
        self.table = table
        self.row_id = row_id
        self.items = None
        self.actions_list = actions_list

        self.combo = QComboBox()
        # self.combo.te
        self.combo.addItems(list(map(lambda x: x.name, self.actions_list)))

        try:
            self.combo.setCurrentIndex(0)
        except Exception as e:
            print("Ind err:", e)

        # print("INDEX:", self.combo.currentIndex())

        if items is not None and len(items) >= 5:
            items = list(map(lambda x: str(x).strip(), items))
            action, i = self.get_action_by_name(items[0])
            # action: AppAction = action  # from coregraphene.auto_actions import AppAction
            if action is not None:
                self.combo.setCurrentIndex(i)
                self.items = [TableItem(self.combo)] + [
                    TableItem(QTableWidgetItem(s)) for s in items[1:]
                ]
                # QTableWidgetItem().setW
                for i, arg in enumerate(action.args_info):
                    if arg.arg_type == list:
                        combo2 = QComboBox()
                        combo2.addItems(arg.arg_list)
                        combo2.setCurrentIndex(max(0, arg.arg_list.index(items[i + 1])))
                        self.items[i + 1] = TableItem(combo2)
                    elif arg.key == "float":
                        widget = AppQDoubleSpinBox()
                        v = 0.0
                        try:
                            v = float(items[i + 1])
                        except:
                            pass
                        widget.setValue(v)
                        widget.setDecimals(arg.decimals if hasattr(arg, 'decimals') else 3)
                        self.items[i + 1] = TableItem(widget)
                    elif arg.key == "time":
                        h, m = 0, 0
                        try:
                            h, m = list(items[i + 1].strip().split(':'))
                            if h:
                                try:
                                    h = int(h)
                                except:
                                    h = 0
                            else:
                                h = 0

                            if m:
                                try:
                                    m = int(m)
                                except:
                                    m = 0
                            else:
                                m = 0

                        except:
                            pass
                        # t: QTime = QTime()
                        # t.setHMS(h, m, 0, 0)
                        # twidget = QTimeEdit()
                        # twidget.setTime(t)

                        text = f"{h}:{m}"
                        twidget = AppQTimeEdit(text=text)

                        self.items[i + 1] = TableItem(twidget)
                    elif arg.key == "int":
                        digit = 0
                        try:
                            digit = int(items[i + 1])
                        except:
                            pass
                        widget = AppQSpinBox()
                        widget.setValue(digit)

                        self.items[i + 1] = TableItem(widget)

        if self.items is None:
            self._set_default_table_items()

        self.combo.currentIndexChanged.connect(self._action_changed)

    def get_action_by_name(self, name):
        for i, action in enumerate(self.actions_list):
            if action.name.strip() == name:
                return action, i
        return None, 0

    def _set_default_table_items(self):
        self.items = [
            TableItem(self.combo),
            TableItem(QTableWidgetItem('')),
            TableItem(QTableWidgetItem('')),
            TableItem(QTableWidgetItem('')),
            TableItem(QTableWidgetItem('')),
        ]

    def __iter__(self):
        self._ind = 0
        return self

    def __next__(self):
        if self._ind < len(self.items):
            x = self.items[self._ind]
            self._ind += 1
            return x
        else:
            raise StopIteration

    def _table_update(self):
        self.table.update_row(self.row_id, self.items)

    def _action_changed(self):
        self._set_default_table_items()
        index = self.combo.currentIndex()
        # print("Update index:", index)
        action = self.actions_list[index]
        for j, arg in enumerate(action.args_info):
            if arg.arg_type == list:
                combo2 = QComboBox()
                combo2.addItems(arg.arg_list)
                combo2.setCurrentIndex(0)
                self.items[j + 1] = TableItem(combo2)
            elif arg.key == "time":
                # self.items[j + 1] = TableItem(QTimeEdit())
                self.items[j + 1] = TableItem(AppQTimeEdit())
            elif arg.key == "int":
                self.items[j + 1] = TableItem(AppQSpinBox())
            elif arg.key == "float":
                widget = AppQDoubleSpinBox()
                widget.setValue(arg.arg_default if arg.arg_default else 0.0)
                widget.setDecimals(arg.decimals if hasattr(arg, 'decimals') else 3)
                self.items[j + 1] = TableItem(widget)
            elif arg.arg_default is not None:
                self.items[j + 1] = TableItem(QTableWidgetItem(str(arg.arg_default)))

        self._table_update()
