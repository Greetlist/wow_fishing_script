from tkinter import Frame
from turtle import position
import cv2
import os
import argh
import sys
import numpy as np
from PIL import Image
import pyautogui
import win32api
import win32con
import time

from PySide6.QtCore import QSize, Qt
from PySide6.QtWidgets import QApplication, QWidget, QMainWindow
from PySide6.QtWidgets import QPushButton

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

class AutoFishingGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Auto Fishing")
        self.setFixedSize(QSize(400, 300))
        self.init_select_rect_button()

    def init_select_rect_button(self):
        self.select_rect_button = QPushButton("Get Rect")
        self.select_rect_button.setCheckable(True)
        self.select_rect_button.clicked.connect(self.get_rect)
        self.setCentralWidget(self.select_rect_button)

    def get_rect(self):
        print('*'*50)
        print('Start to take screen shot')
        print('!'*50)
        mouse_state = 0 # Init state with mouse_up
        win32api.GetAsyncKeyState(win32con.VK_LBUTTON) #refresh GetAsynKeyState function state
        is_finish = False
        while True:
            cur_state = win32api.GetAsyncKeyState(win32con.VK_LBUTTON)
            print('Cur state is : {}'.format(cur_state))
            if cur_state != mouse_state:
                mouse_state = cur_state
                print(mouse_state)
                if mouse_state < 0:
                    print("left mouse down")
                    self.get_mouse_position()
                else:
                    print("left mouse up")
                    self.get_mouse_position()
                    is_finish = True
            if is_finish:
                break
            time.sleep(0.1)

    def get_mouse_position(self):
        x, y = pyautogui.position()
        print('x: {}, y: {}'.format(x, y))

    def init_rect_button(self):
        self.select_rect_button = QPushButton("Select Rect")
        self.select_rect_button.connect()

    #def mousePressEvent(self, e):
    #    print('On Mouse Pressed')

    #def mouseReleaseEvent(self, e):
    #    print('On Mouse Released')

def test_qt():
    app = QApplication(sys.argv)
    gui = AutoFishingGUI()
    gui.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    argh.dispatch_commands([
        test_total,
        test_mask_img,
        get_mouse_position,
        test_qt,
    ])