import datetime

from PyQt5 import QtCore
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QHBoxLayout, QWidget, QMainWindow, QFileDialog

from ..components import LogWidget
from .right_buttons import RightButtonsWidget
from .recipe import RecipeTableWidget
from .base_main_block import BaseMainBlockWidget


class BaseMainDialogWindow(QMainWindow):
    window_title = "CVD-Graphene"
    main_interface_widget_class = BaseMainBlockWidget
    right_buttons_block_class = RightButtonsWidget
    recipe_table_class = RecipeTableWidget
    interface_update_pause = 500

    actions_list = None
    recipe_states = None
    recipe_states_to_str = None
    recipe_table_column_names = None
    notifications_configuration = None

    run_recipe_signal = pyqtSignal()

    def __init__(self, parent=None, system=None):
        super().__init__(parent=parent)
        self.setWindowTitle(self.window_title)

        assert self.actions_list is not None
        assert self.recipe_states is not None
        assert self.recipe_states_to_str is not None
        assert self.recipe_table_column_names is not None
        assert self.notifications_configuration is not None

        ##############################################################################
        # ======================= SYSTEM SETUP + RECIPES =========================== #
        self.system = system
        self._recipe_history = None
        self._current_recipe_step = None
        self._recipe_state = None

        self.base_recipe_init()

        ##############################################################################

        # main_window2 и main_widget2 нужны для иерархии при перемещении
        # виджета над клавиатурой, ибо напрямую перемещать центральный виджет (мы
        # ниже делаем self.setCentralWidget(self.main_widget2) ) -- нельзя,
        # позиция будет обнуляться и будут страдания, проверено за 6 часов потраченного времени
        self._main_window_base = QHBoxLayout()
        self._main_widget_base = QWidget(self)

        self.main_window = QHBoxLayout()
        self.main_widget = QWidget(self._main_widget_base)
        self.main_widget.setObjectName("main_widget")
        # self.main_widget.setStyleSheet("background-color: rgb(240, 220, 255);")
        self.main_widget.setStyleSheet(
            "QWidget#main_widget {background-color: rgb(240, 240, 240);}"
        )
        self.main_widget.setLayout(self.main_window)
        # Устанавливаем центральный виджет Window
        self.setCentralWidget(self._main_widget_base)

        self.main_interface_layout_widget = self.main_interface_widget_class(self)
        self.milw = self.main_interface_layout_widget
        self.main_window.addWidget(self.milw)

        self.set_right_buttons()

        self.setup_interface_update_timer()

        # TABLE WIDGET FOR RECIPE ###################################
        self.set_recipe_table()

        # LOG NOTIFICATION WIDGET ###################################
        self.log = None
        self.log_widget = LogWidget(
            on_close=self.clear_log,
            parent=self,
            notification_types=self.notifications_configuration,
        )
        self.log_widget.move(100, 100)

        # self.threadpool = QThreadPool()
        # print("Multithreading with maximum %d threads" % self.threadpool.maxThreadCount())
        # self.close()

        self.run_recipe_signal.connect(self.run_recipe_ui)

    def system_connect(self):
        """
        Call this function before open full dialog window
        """
        # CONNECT ACTIONS FOR CONTROLLERS ###########################
        self.connect_controllers_actions()

        # RECIPE ####################################################
        self.connect_recipes_actions()

    def base_recipe_init(self):
        self._recipe_history = []
        self._current_recipe_step = None
        self._recipe_state = self.recipe_states.STOP

    def setup_interface_update_timer(self):
        self.timer = QtCore.QTimer()
        self.timer.timeout.connect(self.update_interface_state)
        self.timer.start(self.interface_update_pause)

    def set_right_buttons(self):
        self.right_buttons_layout_widget = self.right_buttons_block_class(
            on_close=self.close,
            on_create_recipe=self.on_create_recipe,
            on_open_recipe=self.on_open_recipe,
            on_stop_recipe=self.system.on_stop_recipe,
            on_pause_recipe=self.system.on_pause_recipe,
            on_get_recipe_state=self.system.get_recipe_state,
            recipe_states=self.recipe_states,
        )
        self.main_window.addWidget(self.right_buttons_layout_widget)

    def set_recipe_table(self):
        self.table_widget = self.recipe_table_class(
            parent=self,
            actions_list=self.actions_list,
            save_recipe_file=self.system.save_recipe_file,
            get_recipe_file_data=self.system.get_recipe_file_data,
            start_recipe=self.start_recipe,
            column_names=self.recipe_table_column_names,
        )

    def connect_controllers_actions(self):
        # ======================= CONNECT FUNCTIONS ========================= #
        pass

    def connect_recipes_actions(self):
        self.system.current_recipe_step_effect.connect(self.add_recipe_step)
        self.system.recipe_start_effect.connect(self.run_recipe_signal.emit)

    def on_create_recipe(self):
        try:
            self.table_widget.on_create_recipe()
        except Exception as e:
            print("On create recipe function error:", e)

    def on_open_recipe(self):
        try:
            file_path = QFileDialog.getOpenFileName(self, 'Выбрать рецепт', '')[0]
            if file_path:
                data = self.system.get_recipe_file_data(file_path)
                self.table_widget.on_open_recipe_file(file_path, data)
        except Exception as e:
            print("On open recipe error:", e)

    def close(self) -> bool:
        self.system.stop()
        return super().close()

    def clear_log(self, uid):
        self.system.clear_log(uid=uid)
        self.log = None

    def __del__(self):
        # print("Window del")
        self.system.destructor()

    def show_time(self):
        print("TIME:", datetime.datetime.now())

    def start_recipe(self):
        try:
            recipe = self.table_widget.get_values()
            self.system.set_recipe(recipe)
            ready = self.system.check_recipe_is_correct()
            # ready = self.system.run_recipe(recipe)
            if not ready:
                return
            self.run_recipe()
        except Exception as e:
            self.system.add_error("Start recipe UI error:" + str(e))
            print("Start recipe UI error:", e)

    def run_recipe(self):
        self.system.run_recipe()
        # self.run_recipe_ui()

    def run_recipe_ui(self):
        self._recipe_history = []
        self.add_recipe_step({'name': "Инициализация рецепта"})
        self.table_widget.on_close()
        self.milw.deactivate_interface()
        self.right_buttons_layout_widget.activate_manage_recipe_buttons()

    def add_recipe_step(self, step: dict):  # name="---", index=None):
        name = step.get('name', '-----')
        index = step.get('index', None)
        index = index if index else len(self._recipe_history)
        if self._current_recipe_step:
            if self._current_recipe_step.get('index', -1) == index:
                return
        self._current_recipe_step = {"name": name, "index": index}
        now_time = datetime.datetime.utcnow()
        now_time_str = f"{now_time.hour}:{now_time.minute}:{now_time.second}"
        self._recipe_history.append(f"{now_time_str} | ШАГ №{index}: {name}")
        try:
            self.milw.set_current_step(self._recipe_history[-1])
        except:
            pass

    def _update_ui_values(self):
        pass

    def memory_snapshot(self):
        pass
        # print("MEMORY:", deep_getsizeof(self, set()))
        # gc.collect()
        # snapshot = tracemalloc.take_snapshot()
        # # snapshot.dump(f'test_{datetime.datetime.now()}.txt')
        #
        # for i, stat in enumerate(snapshot.statistics(f'filename')[:5], 1):
        #     print("top_current", i, str(stat))
        #     # logging.info("top_current", i=i, stat=str(stat))

    def update_interface_state(self):
        try:
            self.memory_snapshot()
            self.system.get_values()
            # recipe_step = self.system.current_recipe_step
            # if recipe_step:
            #     last_recipe_steps = self.system.last_recipe_steps
            #     self.add_recipe_step(**recipe_step)
            recipe_state = self.system.recipe_state
            if recipe_state != self._recipe_state:
                self._recipe_state = recipe_state
                self.milw.set_current_recipe_status(
                    self.recipe_states_to_str.get(self._recipe_state, "UNDEFINED")
                )
                if recipe_state == self.recipe_states.STOP:
                    self.milw.activate_interface()
                    self.right_buttons_layout_widget.deactivate_manage_recipe_buttons()

            self._update_ui_values()

        except Exception as e:
            self.system.add_error(Exception("Ошибка считывания значения: " + str(e)))
            # self.close()
            print("ERROR [get_values_and_log_state]:", e)
        finally:
            try:
                # print("FINALLY:", self.log, "| has logs:",  self.system.has_logs)
                if self.log is None and self.system.has_logs:
                    self.log = self.system.first_log
                    self.log_widget.set_log(self.log)
            except Exception as e:
                print("Set log error:", e)
