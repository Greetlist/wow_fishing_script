# encoding: utf-8
from turtle import position
import cv2
import os
import argh
import sys
import numpy as np
from PIL import Image
import pyautogui
import win32api
import win32gui
import win32con
import time
from ui import MainView

from PySide6.QtCore import QSize, Qt, QRect
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6.QtWidgets import QPushButton, QLineEdit, QLabel
from PySide6.QtWidgets import QGridLayout, QMenu, QCheckBox
from PySide6.QtGui import QPixmap, QScreen, QGuiApplication
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtGui import QCursor, QAction, QIcon
from PySide6.QtGui import QDoubleValidator
from threading import Thread

def deal_single_frame(frame_img):
    img_hsv = cv2.cvtColor(frame_img, cv2.COLOR_BGR2HSV)

    # hsv color need adjust during enviroment or weather changed.
    low_hsv = np.array([0, 35, 0])
    high_hsv = np.array([10, 255, 255])
    img_mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
    img_morph = img_mask.copy()
    cv2.erode(img_morph, (3, 3), img_morph, iterations=2)
    cv2.dilate(img_morph, (3, 3), img_morph, iterations=2)
    cnts, _ = cv2.findContours(img_morph.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    points = np.int0(cv2.boxPoints(rect))
    return cv2.contourArea(c)

def test_total():
    for i in range(0, 75):
        img_path = os.path.join('./imgs/', 'test_{}.png'.format(i))
        frame_img = cv2.imread(img_path)
        print('{}: {}'.format(img_path, deal_single_frame(frame_img)))

def test_mask_img(img_file_name='test_1.png'):
    img_file_path = os.path.join('imgs', img_file_name)
    img_bgr = cv2.imread(img_file_path)
    img_hsv = cv2.cvtColor(img_bgr, cv2.COLOR_BGR2HSV)

    low_hsv = np.array([0, 35, 0])
    high_hsv = np.array([10, 255, 255])
    img_mask = cv2.inRange(img_hsv, low_hsv, high_hsv)

    img_morph = img_mask.copy()
    cv2.erode(img_morph, (3, 3), img_morph, iterations=1)
    cv2.dilate(img_morph, (3, 3), img_morph, iterations=1)

    cnts, _ = cv2.findContours(img_morph.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts) < 1:
        print("cannot find rect")
        cv2.destroyAllWindows()
        return

    c = max(cnts, key=cv2.contourArea)
    rect = cv2.minAreaRect(c)
    points = np.int0(cv2.boxPoints(rect))
    print(points)
    cv2.drawContours(img_hsv, [points], -1, (0, 0, 255), 1)

    cv2.imshow('hsv', img_hsv)
    cv2.imshow('mask', img_mask)
    cv2.imshow('morph', img_morph)
    cv2.waitKey(0)
    cv2.destroyAllWindows()

def get_mouse_position():
    x, y = pyautogui.position()
    print('x: {}, y: {}'.format(x, y))

#class ScreenShotMainWidget(QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)
#        self.parent = parent
#        self.capture_total_screen()
#        self.init_window()
#        self.init_screenshot_menu()
#        self.mouse_press = False
#
#    def capture_total_screen(self):
#        total_screens = QGuiApplication.screens() #main screen's index is 0
#        self.max_height = 0
#        self.total_width = 0
#        for screen in total_screens:
#            screen_rect = screen.geometry()
#            self.max_height = max(self.max_height, screen_rect.height())
#            self.total_width += screen_rect.width()
#
#        cur_pixmap = QPixmap(QSize(self.total_width, self.max_height))
#        painter = QPainter(cur_pixmap)
#        blank_color = QColor(0, 0, 0, 0)
#        painter.fillRect(cur_pixmap.rect(), blank_color)
#        for screen in total_screens:
#            screen_pixmap = screen.grabWindow(0)
#            screen_rect = screen.geometry()
#            painter.drawPixmap(screen_rect, screen_pixmap)
#        painter.end()
#        self.origin_pixmap = cur_pixmap
#
#    def init_window(self):
#        self.setMouseTracking(True)
#        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
#        self.setWindowState(Qt.WindowActive | Qt.WindowFullScreen)
#
#    def init_screenshot_menu(self):
#        self.menu = QMenu(self)
#        confirm_action = QAction(QIcon('static/check.png'), "Confirm", self)
#        confirm_action.setCheckable(True)
#        confirm_action.triggered.connect(self.finish_screenshot)
#        self.menu.addAction(confirm_action)
#
#    def paintEvent(self, e):
#        painter = QPainter(self)
#        shadow_color = QColor(0, 0, 0, 100)
#        pen = QPen(QColor(255, 0, 0, 255), 3, Qt.SolidLine, Qt.SquareCap)
#        painter.setPen((pen))
#
#        painter.drawPixmap(self.origin_pixmap.rect(), self.origin_pixmap)
#        painter.fillRect(self.origin_pixmap.rect(), shadow_color)
#
#        if (self.mouse_press):
#            left, top, right, bottom = self.calc_real_rect()
#            cur_rect = QRect(left, top, right - left, bottom - top)
#            cur_captured_pixmap = self.origin_pixmap.copy(cur_rect)
#            painter.drawPixmap(cur_rect.topLeft(), cur_captured_pixmap)
#            painter.drawRect(cur_rect)
#            pen.setColor(QColor(255, 255, 255, 255))
#            painter.setPen(pen)
#            painter.drawText(
#                left + 2, top - 5, 
#                "{} X {}".format(right - left, bottom - top)
#            )
#        painter.end()
#
#    def calc_real_rect(self):
#        real_left = self.start_x if self.start_x < self.end_x else self.end_x
#        real_top = self.start_y if self.start_y < self.end_y else self.end_y
#        real_right = self.end_x if self.start_x < self.end_x else self.start_x
#        real_bottom = self.end_y if self.start_y < self.end_y else self.start_y
#        return real_left, real_top, real_right, real_bottom
#
#    def keyPressEvent(self, e):
#        if (e.key() == Qt.Key_Escape):
#            print('Press Escape, Close')
#            self.close()
#        elif (e.key() == Qt.Key_Return):
#            print('Press Enter, Finish ScreenShot')
#            self.close()
#
#    def mousePressEvent(self, e):
#        self.mouse_press = True
#        self.start_x = e.globalPosition().x()
#        self.start_y = e.globalPosition().y()
#
#    def mouseReleaseEvent(self, e):
#        self.mouse_press = False
#        self.menu.exec(QCursor.pos())
#
#    def mouseMoveEvent(self, e):
#        if self.mouse_press:
#            self.end_x = e.globalPosition().x()
#            self.end_y = e.globalPosition().y()
#            self.update() #force invoke painterEvent
#
#    def finish_screenshot(self):
#        left, top, right, bottom = self.calc_real_rect()
#        print('left: {left}, top: {top}, right: {right}, bottom: {bottom}'.format(**locals()))
#        self.close()
#
#    def get_captured_pixmap_rect(self):
#        left, top, right, bottom = self.calc_real_rect()
#        return {
#            'left': left,
#            'top': top,
#            'right': right,
#            'bottom': bottom,
#            'width': right - left,
#            'height': bottom - top,
#        }
#
#    def closeEvent(self, e):
#        self.parent.set_edit_data(self.get_captured_pixmap_rect())
#
#class ScreenShotCoordinateView(QWidget):
#    def __init__(self, parent=None):
#        super().__init__(parent)
#        self.edit_dict = {
#            'left': dict(),
#            'top': dict(),
#            'right': dict(),
#            'bottom': dict(),
#            'width': dict(),
#            'height': dict(),
#        }
#        self.init_button()
#        self.init_child_widget()
#
#    def init_button(self):
#        self.rect_button = QPushButton("Get Fish Area")
#        self.rect_button.setCheckable(True)
#        #self.rect_button.clicked.connect(self.determine_rect)
#        self.rect_button.clicked.connect(self.show_screenshot_dialog)
#
#    def show_screenshot_dialog(self):
#        widget = ScreenShotMainWidget(self)
#        widget.show()
#        widget.setFixedSize(QSize(widget.total_width, widget.max_height)) #must invoke after show() function.
#
#    def determine_rect(self):
#        mouse_state = 0 # Init state with mouse_up
#        win32api.GetAsyncKeyState(win32con.VK_LBUTTON) #refresh GetAsynKeyState function state
#        is_finish = False
#        while True:
#            cur_state = win32api.GetAsyncKeyState(win32con.VK_LBUTTON)
#            if cur_state != mouse_state:
#                mouse_state = cur_state
#                if mouse_state < 0:  #press left mouse
#                    x, y = self.get_mouse_position()
#                    self.edit_dict['left']['real_data'] = x
#                    self.edit_dict['left']['edit_instance'].setText(str(x))
#                    self.edit_dict['top']['real_data'] = y
#                    self.edit_dict['top']['edit_instance'].setText(str(y))
#                else: #release left mouse
#                    x, y = self.get_mouse_position()
#                    self.edit_dict['right']['real_data'] = x
#                    self.edit_dict['right']['edit_instance'].setText(str(x))
#                    self.edit_dict['bottom']['real_data'] = y
#                    self.edit_dict['bottom']['edit_instance'].setText(str(y))
#                    is_finish = True
#            if is_finish:
#                height = self.edit_dict['bottom']['real_data'] - self.edit_dict['top']['real_data']
#                width = self.edit_dict['right']['real_data'] - self.edit_dict['left']['real_data']
#                self.edit_dict['height']['real_data'] = height
#                self.edit_dict['height']['edit_instance'].setText(str(height))
#                self.edit_dict['width']['real_data'] = width
#                self.edit_dict['width']['edit_instance'].setText(str(width))
#                break
#            time.sleep(0.1)
#
#    def get_mouse_position(self):
#        x, y = pyautogui.position()
#        return x, y
#
#    def init_child_widget(self):
#        self.g_layout = QGridLayout()
#        self.setLayout(self.g_layout)
#
#        self.g_layout.addWidget(self.rect_button, 0, 0, 1 ,4)
#        row = 1
#        for data_str, _ in self.edit_dict.items():
#            cur_edit = QLineEdit(self)
#            cur_label = QLabel(data_str + ':', self)
#            cur_label.setBuddy(cur_edit)
#            validator = QDoubleValidator(self)
#            cur_edit.setValidator(validator)
#            self.g_layout.addWidget(cur_label, row, 0)
#            self.g_layout.addWidget(cur_edit, row, 1)
#            row += 1
#            self.edit_dict[data_str]['edit_instance'] = cur_edit
#            self.edit_dict[data_str]['real_data'] = 0
#
#    def set_edit_data(self, data_dict):
#        for data_str, _ in self.edit_dict.items():
#            self.edit_dict[data_str]['real_data'] = data_dict[data_str]
#            self.edit_dict[data_str]['edit_instance'].setText(str(data_dict[data_str]))
#
#    def get_capture_coordinate(self):
#        res = {}
#        for data_str, _ in self.edit_dict.items():
#            res[data_str] = self.edit_dict[data_str]['real_data']
#        return res
#
#class MainView(QWidget):
#    def __init__(self, parent=None):
#        super().__init__()
#        self.init_child_widget()
#
#    def init_child_widget(self):
#        self.screeshot_view = ScreenShotCoordinateView(self)
#        self.functional_view = FunctionalView(self)
#
#        self.start_button = QPushButton("Start Fishing")
#        self.start_button.setCheckable(True)
#        self.start_button.clicked.connect(self.start_fishing)
#
#        self.stop_button = QPushButton("Stop")
#        self.stop_button.setCheckable(True)
#        self.stop_button.clicked.connect(self.stop_fishing)
#
#        self.g_layout = QGridLayout()
#        self.setLayout(self.g_layout)
#        self.g_layout.addWidget(self.screeshot_view, 0, 0)
#        self.g_layout.addWidget(self.functional_view, 0, 1)
#        self.g_layout.addWidget(self.start_button, 1, 0)
#        self.g_layout.addWidget(self.stop_button, 1, 1)
#
#    def start_fishing(self):
#        functional_config = self.functional_view.get_all_config_data()
#        capture_area_coordinate = self.screeshot_view.get_capture_coordinate()
#        self.fishing_instance = FishingHelper(functional_config, capture_area_coordinate)
#        running_thread = Thread(self.fishing_instance.start())
#        running_thread.start()
#
#    def stop_fishing(self):
#        self.fishing_instance.stop()
#
#    def resize_and_show(self):
#        self.show()
#        self.setFixedSize(QSize(500, 400))

def test_qt():
    app = QApplication(sys.argv)
    #gui = ScreenShotCoordinateView()
    gui = MainView.MainView()
    gui.resize_and_show()
    sys.exit(app.exec_())

def test_send_key():
    window_name = "test.txt - 记事本"
    target_window = win32gui.FindWindow(None, window_name)
    #child_window = win32gui.GetWindow(target_window, win32con.GW_CHILD)

    for i in range(100):
        #win32gui.PostMessage(child_window, win32con.WM_KEYDOWN, 0x31, 0)
        #win32gui.PostMessage(child_window, win32con.WM_KEYUP, 0x31, 0)
        win32gui.PostMessage(target_window, win32con.WM_CHAR, 0x31, 0)
        time.sleep(1)

if __name__ == '__main__':
    argh.dispatch_commands([
        test_total,
        test_mask_img,
        get_mouse_position,
        test_qt,
        test_send_key,
    ])