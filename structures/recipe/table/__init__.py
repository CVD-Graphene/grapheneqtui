import os
import string
import time
import uuid

from random import choice
from PyQt5 import QtCore
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QGridLayout, QWidget, QFileDialog, \
    QTableWidget, QLineEdit, QPushButton, QHBoxLayout, QHeaderView
from PyQt5.QtCore import QSize

from .cells import (TableItem, AppQSpinBox, AppQDoubleSpinBox, AppQTimeEdit,)
from .row import TableRow
from .styles import styles


def random_str(length=5):
    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    return ''.join(choice(letters) for _ in range(length))


def create_recipe_file_name():
    return "recipe_" + random_str()


custom_font = QFont()
custom_font.setPointSize(18)

CONTENT_COLUMN_AMOUNT = 5
DELETE_ROW_BUTTON_COLUMN_INDEX = CONTENT_COLUMN_AMOUNT
ADD_UP_ROW_BUTTON_COLUMN_INDEX = DELETE_ROW_BUTTON_COLUMN_INDEX + 1

TOTAL_COLUMNS_AMOUNT = ADD_UP_ROW_BUTTON_COLUMN_INDEX + 1


class RecipeTableWidget(QWidget):

    def __init__(self,
                 parent=None,
                 actions_list=None,
                 save_recipe_file=None,
                 get_recipe_file_data=None,
                 start_recipe=None,
                 column_names=None,
                 ):
        # You must call the super class method
        super().__init__(parent)

        self.column_names = column_names
        assert self.column_names is not None

        self.actions_list = actions_list

        self.save_recipe_file = save_recipe_file
        self.get_recipe_file_data = get_recipe_file_data
        self.start_recipe = start_recipe

        self.file = None
        self.path = None

        self.file_path = None  # for directly open files

        self.setObjectName("AppTableWidget")
        self.setStyleSheet(styles.container)
        self.setAttribute(QtCore.Qt.WA_StyledBackground, True)

        # central_widget = QWidget(self)  # Create a central widget
        # self.setCentralWidget(central_widget)  # Install the central widget

        grid_layout = QGridLayout()  # Create QGridLayout
        self.setLayout(grid_layout)
        # QApplication.desktop().width(),
        # QApplication.desktop().height()

        self.setFont(custom_font)

        self.setMinimumSize(QSize(
            QApplication.desktop().width() * 0.99,
            QApplication.desktop().height() * 0.99
        ))  # Set sizes
        self.row_count = 1
        self.rows = [TableRow(table=self, row_id=uuid.uuid4(), actions_list=self.actions_list)]

        table = QTableWidget()  # Create a table
        table.setColumnCount(TOTAL_COLUMNS_AMOUNT)  # Set three columns
        table.setRowCount(self.row_count)  # and one row
        table.setFont(custom_font)
        # table.setWordWrap(False)  # ABOUT WORD WRAP: https://stackoverflow.com/questions/53759776/pyqt-qtablewidget-wordwrap-lines

        # Set the table headers
        table.setHorizontalHeaderLabels(self.column_names)

        # self.combo = QComboBox()
        # self.combo.te
        # self.combo.addItems(["option1", "option2", "option3", "option4"])
        # self.comboBox.currentIndexChanged.connect(slotLambda)

        # Set the tooltips to headings
        table.horizontalHeaderItem(0).setToolTip("Процесс")
        table.horizontalHeaderItem(1).setToolTip("Аргумент")
        table.horizontalHeaderItem(2).setToolTip("Аргумент")
        table.horizontalHeaderItem(3).setToolTip("Аргумент")
        table.horizontalHeaderItem(4).setToolTip("Комментарий")

        # Set the alignment to the headers
        # table.horizontalHeaderItem(0).setTextAlignment(Qt.AlignLeft)
        # # table.horizontalHeaderItem(1).setTextAlignment(Qt.AlignHCenter)
        # table.horizontalHeaderItem(4).setTextAlignment(Qt.AlignRight)

        self.table = table

        add_row_button = QPushButton('+ добавить строку')
        add_row_button.clicked.connect(self._add_row)
        add_row_button.setObjectName("table_button")
        add_row_button.setStyleSheet(styles.table_button)

        # get_values_button = QPushButton('print values')
        # get_values_button.clicked.connect(self.get_values)
        buttons_layout = QHBoxLayout()

        save_button = QPushButton("SAVE RECIPE")
        save_button.clicked.connect(self.save_recipe)
        save_button.setObjectName("table_button")
        save_button.setStyleSheet(styles.table_button)

        close_button = QPushButton("CLOSE")
        close_button.clicked.connect(self.on_close)
        close_button.setObjectName("table_button")
        close_button.setStyleSheet(styles.table_button)

        start_button = QPushButton("RUN RECIPE")
        start_button.clicked.connect(self.start_recipe)
        start_button.setObjectName("table_button")
        start_button.setStyleSheet(styles.table_button)

        name = QLineEdit()
        name.setPlaceholderText("Название файла...")
        name.setText(create_recipe_file_name())
        self.file_name_widget = name
        self.file_name_widget.setObjectName("table_name_input")
        self.file_name_widget.setStyleSheet(styles.table_name_input)

        buttons_layout.addWidget(self.file_name_widget)
        buttons_layout.addWidget(save_button)
        buttons_layout.addWidget(start_button)
        # buttons_layout.addWidget(get_values_button)
        buttons_layout.addWidget(close_button)

        grid_layout.addLayout(buttons_layout, 0, 0)
        grid_layout.addWidget(table, 1, 0)  # Adding the table to the grid
        grid_layout.addWidget(add_row_button, 2, 0)
        # grid_layout.addWidget(get_values_button, 1, 1)

        self._update_table()
        self.hide()

    def _update_table_ui(self):
        horizontalHeader = self.table.horizontalHeader()
        # resize the first column to 100 pixels
        for i in range(CONTENT_COLUMN_AMOUNT - 1):
            horizontalHeader.resizeSection(i, 195)
            horizontalHeader.setFont(custom_font)
        # adjust the second column to its contents
        # horizontalHeader.setSectionResizeMode(
        #     1, QHeaderView.ResizeToContents)
        # adapt the third column to fill all available space
        # horizontalHeader.setSectionResizeMode(
        #     4, QHeaderView.Stretch)
        # Do the resize of the columns by content
        self.table.resizeColumnsToContents()
        horizontalHeader.setSectionResizeMode(
            CONTENT_COLUMN_AMOUNT - 1, QHeaderView.Stretch)
        for i in range(CONTENT_COLUMN_AMOUNT, TOTAL_COLUMNS_AMOUNT):
            horizontalHeader.resizeSection(i, 50)
            # horizontalHeader.setSectionResizeMode(i, QHeaderView.Stretch)

        for i in range(self.row_count):
            self.table.setRowHeight(i, 48)

    def on_create_recipe(self):
        self.show()
        print("On create recipe show!!!")

    def on_open_recipe_file(self, file_path, data):
        try:
            self.file_path = file_path
            self.row_count = len(data)
            self.table.setRowCount(self.row_count)
            self.rows = []
            for i, row in enumerate(data):
                # table_row = TableRow(table=self, row_id=i, items=row, actions_list=self.actions_list)
                table_row = TableRow(table=self, row_id=uuid.uuid4(), items=row, actions_list=self.actions_list)
                self.rows.append(table_row)
            self._update_table()
            # self.rows = [TableRow(table=self, row_id=0, actions_list=self.actions_list)]
            file_name = os.path.basename(file_path)
            self.file_name_widget.setText(file_name)
            self.file_name_widget.setEnabled(False)
            self.show()
        except Exception as e:
            print("Open recipe file error UI:", e)

    def set_target_file(self, path=None, file=None):
        self.file = file
        self.path = path

    def on_delete_row(self, unique_id):
        delete_row_index = -1
        for i, row_obj in enumerate(self.rows):
            if row_obj.row_id == unique_id:
                delete_row_index = i
                break

        print('Delete row', unique_id, 'with index:', delete_row_index)
        if delete_row_index < 0:
            return

        new_rows = list(filter(lambda x: x.row_id != unique_id, self.rows))
        self.rows = new_rows
        self.row_count = len(self.rows)
        # self.table.setRowCount(self.row_count)  # and one row
        self.table.removeRow(delete_row_index)

        # for i, row in enumerate(self.rows[delete_row_index:]):
        #     self.update_row(row.row_id, row, row_index=i + delete_row_index)

        self._update_table_ui()

    def update_row(self, row_id, items, row_index=None):
        if row_index is None:
            row_index = -1
            for row_i, row_obj in enumerate(self.rows):
                if row_obj.row_id == row_id:
                    row_index = row_i
                    break
            print('new row index:', row_index)
            if row_index < 0:
                return

        for i, item in enumerate(items):
            if item.is_item:
                try:
                    self.table.removeCellWidget(row_index, i)
                    # self.table.cellW
                except:
                    pass
                self.table.setItem(row_index, i, item.widget.clone())
            else:
                self.table.setCellWidget(row_index, i, item.widget)

        delete_button = QPushButton('🗑️')

        def on_delete():
            self.on_delete_row(row_id)

        delete_button.clicked.connect(on_delete)
        self.table.setCellWidget(row_index, DELETE_ROW_BUTTON_COLUMN_INDEX, delete_button)

        self.table.setCellWidget(row_index, ADD_UP_ROW_BUTTON_COLUMN_INDEX, QPushButton('↑'))

    def _update_table(self):
        self.row_count = len(self.rows)
        self.table.setRowCount(self.row_count)  # and one row

        for i, row in enumerate(self.rows):
            self.update_row(row.row_id, row, row_index=i)

        self._update_table_ui()
        # self.table.resizeColumnsToContents()

    def _add_row(self):
        # self.row_count += 1
        # self.table.setRowCount(self.row_count)  # and one row
        # self.rows.append(TableRow(table=self, row_id=self.row_count, actions_list=self.actions_list))
        self.rows.append(TableRow(table=self, row_id=uuid.uuid4(), actions_list=self.actions_list))
        self._update_table()

    def get_values(self):
        try:
            arr = []
            for row in range(self.table.rowCount()):
                row_arr = []
                for col in range(CONTENT_COLUMN_AMOUNT):
                    it = self.table.item(row, col)
                    it2 = self.table.cellWidget(row, col)
                    if it2 is not None:
                        if isinstance(it2, AppQTimeEdit):  # QTimeEdit
                            # if hasattr(it2, 'time'):
                            #     t: QTime = it2.time()
                            # t.setHMS(1, 1, 0, 0)
                            # print("TIME SAVE:", t.hour(), t.minute(), t.second())
                            # row_arr.append(f"{t.hour()}:{t.minute()}")
                            row_arr.append(f"{it2.text()}")
                            continue
                        elif isinstance(it2, AppQDoubleSpinBox):
                            row_arr.append(f"{it2.value()}")
                            continue
                        elif isinstance(it2, AppQSpinBox):
                            row_arr.append(f"{it2.value()}")
                            continue

                        row_arr.append(it2.currentText())
                        continue
                    if it is None:
                        row_arr.append('')
                        continue

                    if hasattr(it, 'text'):
                        row_arr.append(it.text())
                    elif hasattr(it, 'currentText'):
                        row_arr.append(it.currentText())
                arr.append(row_arr)
            # print("TABLE:", arr)
            return arr

        except Exception as e:
            print("Err get value table:", e)

    def save_recipe(self):
        try:
            has_file_path = bool(self.file_path)

            if not self.path and not has_file_path:
                path = QFileDialog.getExistingDirectory(self, "Выберите папку", "")
                if path:
                    self.path = path
                else:
                    return
            file_name = self.file_name_widget.text()
            if file_name.endswith('.xlsx'):
                self.file = file_name
            else:
                self.file = file_name + '.xlsx'

            arr = self.get_values()
            self.save_recipe_file(
                file=self.file,
                path=self.path,
                file_path=self.file_path,
                data=arr
            )
        except Exception as e:
            print("Save file error:", e)

    def on_close(self):
        self.file = None
        self.path = None
        self.file_path = None
        self.file_name_widget.setText(create_recipe_file_name())
        self.file_name_widget.setEnabled(True)
        self.hide()

        # self.row_count = 1
        self.rows = [TableRow(table=self, row_id=uuid.uuid4(), items=None, actions_list=self.actions_list)]
        # self.table.setRowCount(self.row_count)  # and one row
        self._update_table()
