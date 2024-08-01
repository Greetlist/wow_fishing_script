from ui import ScreenShotCoordinateView
from ui import FunctionalView, DebugHSVColorView
import FishingHelper
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout, QTextBrowser
from PySide6.QtCore import QSize
import FishingThread
import DebugHSVColorThread
import LogFetcherThread
from PySide6 import QtWidgets
import cv2
import numpy as np
import queue

class MainView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_child_widget()
        self.init_log_fetch_thread()

    def init_child_widget(self):
        self.screeshot_view = ScreenShotCoordinateView.ScreenShotCoordinateView(self)
        self.functional_view = FunctionalView.FunctionalView(self)

        self.start_button = QPushButton("Start Fishing")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_fishing)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setCheckable(True)
        self.stop_button.clicked.connect(self.stop_fishing)
        self.stop_button.setEnabled(False)

        self.debug_hsv_view = DebugHSVColorView.DebugHSVColorView()
        self.debug_hsv_view.set_click_function(self.start_debug_hsv_color)

        self.g_layout = QGridLayout()
        self.setLayout(self.g_layout)
        self.g_layout.addWidget(self.screeshot_view, 0, 0)
        self.g_layout.addWidget(self.functional_view, 0, 1)
        self.g_layout.addWidget(self.debug_hsv_view, 1, 0)
        self.g_layout.addWidget(self.start_button, 2, 0)
        self.g_layout.addWidget(self.stop_button, 2, 1)

        self.log_browser = QTextBrowser()
        self.g_layout.addWidget(self.log_browser, 3, 0, 1, 4)

    def start_fishing(self):
        functional_config = self.functional_view.get_all_config_data()
        capture_area_coordinate = self.screeshot_view.get_capture_coordinate()
        min_list, max_list = self.debug_hsv_view.get_list()
        print(min_list, max_list)
        fishing_helper = FishingHelper.FishingHelper(functional_config, capture_area_coordinate, min_list, max_list)
        self.fish_thread = FishingThread.FishingThread(fishing_helper, self)
        self.fish_thread.start()
        self.start_button.setText("Fishing")
        self.start_button.setEnabled(False)
        self.stop_button.setEnabled(True)

    def stop_fishing(self):
        if self.fish_thread.isRunning():
            self.fish_thread.terminate()
            self.stop_button.setText("Stoping...")
            self.stop_button.setEnabled(False)
            self.fish_thread.wait()
            self.stop_button.setText("Stop")
            self.start_button.setText("Start Fishing")
            self.start_button.setEnabled(True)

    def start_debug_hsv_color(self):
        functional_config = self.functional_view.get_all_config_data()
        capture_area_coordinate = self.screeshot_view.get_capture_coordinate()
        fishing_helper = FishingHelper.FishingHelper(functional_config, capture_area_coordinate)
        result_queue = queue.Queue()
        self.debug_hsv_thread = DebugHSVColorThread.DebugHSVColorThread(fishing_helper, self, result_queue)
        self.debug_hsv_thread.start()
        data_dict = {
            "min_list": result_queue.get(),
            "max_list": result_queue.get(),
        }
        self.debug_hsv_thread.wait()
        self.debug_hsv_view.set_edit_data(data_dict)

    def reset_fishing_button(self):
        self.stop_button.setText("Stop")
        self.stop_button.setEnabled(False)
        self.start_button.setText("Start Fishing")
        self.start_button.setEnabled(True)

    def resize_and_show(self):
        self.setWindowTitle("Auto Fishing")
        self.show()
        self.setFixedSize(QSize(800, 450))

    def init_log_fetch_thread(self):
        self.log_fetch_thread = LogFetcherThread.LogFetcherThread(self)
        self.log_fetch_thread.start()

    def append_text(self, text):
        if text is not None:
            self.log_browser.append(text)

    def closeEvent(self, e):
        self.log_fetch_thread.terminate()

    #def moveEvent(self, e):
    #    old_screen = QtWidgets.QApplication.screenAt(e.oldPos())
    #    new_screen = QtWidgets.QApplication.screenAt(e.pos())
    #    if old_screen != new_screen:
    #        print(old_screen, new_screen)
    #    return super().moveEvent(e)