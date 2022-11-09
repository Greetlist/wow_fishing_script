import win32gui
import pyautogui
import os
import time
import cv2
import numpy as np
import sys
import datetime as dt
from threading import Lock

class FishingHelper:
    def __init__(self, functional_config, capture_area_coordinate) -> None:
        self.wow_window_name = "魔兽世界" # need to be utf-8
        self.wow_window = None
        self.windown_rect = dict()

        # core member
        self.last_float_area = 0
        self.last_mid_x = 0
        self.last_mid_y = 0
        self.fish_float_x = 0
        self.fish_float_y = 0
        self.stop = True
        self.wait_bite_time = 0.1 # unit: second
        self.last_cast_time = 0

        self.stop_lock = Lock()

        self.init_functional_config(functional_config)
        self.init_capture_area(capture_area_coordinate)

    def init_functional_config(self, functional_config):
        self.use_coordinate = functional_config['use_coordinate']
        self.use_area = not self.use_coordinate
        self.enable_to_work_time = functional_config['enable_to_work_time']  # unit: second
        self.rest_time = functional_config['enable_to_work_time'] # unit: second
        self.float_area_changed_threshold = 45
        self.float_coordinate_changed_threshold = float(functional_config['float_coordinate_changed_threshold'])
        self.cast_period = functional_config['cast_period'] # unit: second

    def init_capture_area(self, capture_area_coordinate):
        self.capture_left = capture_area_coordinate['left']
        self.capture_top = capture_area_coordinate['top']
        self.capture_right = capture_area_coordinate['right']
        self.capture_bottom = capture_area_coordinate['bottom']
        self.capture_width = capture_area_coordinate['width']
        self.capture_height = capture_area_coordinate['height']

    def reset_all_condition(self):
        self.last_float_area = 0
        self.last_mid_x = 0
        self.last_mid_y = 0
        self.fish_float_x = 0
        self.fish_float_y = 0

    def init(self):
        self.wow_window = win32gui.FindWindow(None, self.wow_window_name)
        if self.wow_window is None:
            print("Cannot find window name: {}".format(self.wow_window_name))
            return False
        left, top, right, bottom = win32gui.GetWindowRect(self.wow_window)
        self.windown_rect['left'] = left
        self.windown_rect['top'] = top
        self.windown_rect['right'] = right
        self.windown_rect['bottom'] = bottom
        print('Windown rect is : {}'.format(self.windown_rect))
        return True

    def start(self):
        while True:
            self.cast_some_skill()
            self.start_fishing()
            while not self.is_bite_hook():
                time.sleep(self.wait_bite_time)
            while not self.is_wow_foreground_window():
                time.sleep(self.enable_to_work_time)
            self.get_fish()
            self.reset_all_condition()
            self.stop_lock.acquire()
            if self.stop:
                self.stop_lock.release()
                return
            self.stop_lock.release()
            time.sleep(self.rest_time)

    def start_fishing(self):
        if not self.is_wow_foreground_window():
            time.sleep(5)
        pyautogui.press('1') # bind fish skill to main ```action-bar``` number 1
        time.sleep(2) # sleep for a while to find fish_float
        self.find_fish_float()

    def is_bite_hook(self):
        cur_img = self.capture_main_fishing_screen()
        cur_contour = self.get_frame_contours(cur_img)
        cur_area = cv2.contourArea(cur_contour)
        if self.use_area:
            print(
                'last_area: [{}], cur_area: [{}], abs(last - cur): [{}]'.format(
                    self.last_float_area,
                    cur_area,
                    abs(self.last_float_area - cur_area)
                )
            )
            if self.last_float_area > 0 and abs(self.last_float_area - cur_area) > self.float_area_changed_threshold:
                return True
            self.last_float_area = cur_area
            return False
        elif self.use_coordinate:
            cur_moments = cv2.moments(cur_contour)
            if cur_moments['m00'] != 0:
                cur_x = int(cur_moments['m10'] / cur_moments['m00'])
                cur_y = int(cur_moments['m01'] / cur_moments['m00'])
                abs_sub_x = abs(self.last_mid_x - cur_x)
                abs_sub_y = abs(self.last_mid_y - cur_y)
                print(
                    'last_x: {}, last_y: {}, cur_x: {}, cur_y: {}, abs(sub_x): [{}], abs(sub_y): [{}]'.format(
                        self.last_mid_x, self.last_mid_y, cur_x, cur_y, abs_sub_x, abs_sub_y
                    )
                )
                if (self.last_mid_x > 0 and self.last_mid_y > 0) and \
                    (abs_sub_x * abs_sub_x + abs_sub_y * abs_sub_y > self.float_coordinate_changed_threshold):
                    return True
                self.last_mid_x = cur_x
                self.last_mid_y = cur_y
            return False

    # (low_hsv, hight_hsv) color need adjust during enviroment or weather changed.
    def get_frame_contours(self, frame_img):
        img_hsv = cv2.cvtColor(frame_img, cv2.COLOR_BGR2HSV)
        low_hsv = np.array([0, 35, 0])
        high_hsv = np.array([10, 255, 255])
        img_mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
        img_morph = img_mask.copy()
        cv2.erode(img_morph, (3, 3), img_morph, iterations=2)
        cv2.dilate(img_morph, (3, 3), img_morph, iterations=2)
        cnts, _ = cv2.findContours(img_morph.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts, key=cv2.contourArea)
        #rect = cv2.minAreaRect(c)
        #points = np.int0(cv2.boxPoints(rect))
        #print(points)
        #cv2.drawContours(img_hsv, [points], -1, (0, 0, 255), 1)

        #cv2.imshow('hsv', img_hsv)
        #cv2.imshow('mask', img_mask)
        #cv2.imshow('morph', img_morph)
        #cv2.waitKey(0)
        #cv2.destroyAllWindows()
        #sys.exit(0)
        return c

    def capture_main_fishing_screen(self):
        main_screen_region = (
            self.capture_left,
            self.capture_top,
            self.capture_width,
            self.capture_height,
        )
        cur_screenshot = pyautogui.screenshot(region=main_screen_region)
        #remember to convert data type
        cur_captured_img = cv2.cvtColor(np.array(cur_screenshot), cv2.COLOR_RGB2BGR)
        return cur_captured_img

    def find_fish_float(self):
        cur_img = self.capture_main_fishing_screen()
        contour = self.get_frame_contours(cur_img)
        cur_moments = cv2.moments(contour)
        if cur_moments['m00'] != 0:
            self.fish_float_x = int(cur_moments['m10'] / cur_moments['m00']) + self.capture_left
            self.fish_float_y = self.capture_top + int(cur_moments['m01'] / cur_moments['m00'])

    def get_fish(self):
        pyautogui.click(self.fish_float_x, self.fish_float_y)
        pyautogui.rightClick(self.fish_float_x, self.fish_float_y)

    def stop(self):
        self.stop_lock.acquire()
        self.stop = True
        self.stop_lock.release()

    def is_wow_foreground_window(self):
        return win32gui.GetForegroundWindow() == self.wow_window

    def cast_some_skill(self):
        if self.last_cast_time == 0 or time.time() - self.last_cast_time > self.cast_period:
            pyautogui.press('6')
            self.last_cast_time = time.time()
            time.sleep(self.enable_to_work_time)

    def test(self):
        for i in range(0, 75):
            cur_img = self.capture_main_fishing_screen()
            cur_img.save('imgs/test_{}.png'.format(i))
            time.sleep(0.1)