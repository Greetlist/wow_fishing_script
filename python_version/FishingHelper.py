import win32gui
import win32con
import pyautogui
import time
import cv2
import numpy as np
import mss
from Logger import FishingLogger
import traceback

import constant
import util

class FishingHelper:
    def __init__(self, functional_config, capture_area_coordinate) -> None:
        self.init_functional_config(functional_config)
        self.init_capture_area(capture_area_coordinate)
        self.init_key_binding()
        assert self.init(), "Init Not Success"

        # core member
        self.last_float_area = 0
        self.last_mid_x = 0
        self.last_mid_y = 0
        self.fish_float_x = 0
        self.fish_float_y = 0
        self.wait_bite_time = 0.1 # unit: second
        self.last_cast_time = 0

        self.start_fishing_time = 0
        self.tolerate_time = 20 #second

        self.current_fishing_count = 0

    def init_key_binding(self):
        self.fish_key = 0x31 #key_board 1
        self.get_fish_key = 0x39 #key_board 9

    def init_functional_config(self, functional_config):
        self.wow_window_name = functional_config['wow_window_name'] # need to be utf-8
        self.wow_window = None
        self.use_coordinate = functional_config['use_coordinate']
        self.use_area = not self.use_coordinate
        self.enable_to_work_time = functional_config['enable_to_work_time']  # unit: second
        self.rest_time = functional_config['rest_time'] # unit: second
        self.float_area_changed_threshold = 45
        self.float_coordinate_changed_threshold = float(functional_config['float_coordinate_changed_threshold'])
        self.cast_period = functional_config['cast_period'] # unit: second
        self.is_cast_periodically = functional_config['is_cast_periodically'] # unit: second
        self.is_test = functional_config['is_test']
        self.is_foreground = functional_config['is_foreground']
        self.float_offset = functional_config['float_offset']
        self.jump_ratio = functional_config['jump_ratio']
        self.max_fishing_count = functional_config['max_fishing_count']

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
            FishingLogger.error("Cannot find window name: {}".format(self.wow_window_name))
            return False
        return True

    def start(self):
        while True:
            try:
                if self.is_cast_periodically:
                    self.cast_some_skill()
                self.random_jump()
                self.start_fishing()
                while not self.is_over_tolerate_time() and not self.is_bite_hook():
                    time.sleep(self.wait_bite_time)
                while self.is_foreground and not self.is_wow_foreground_window():
                    time.sleep(self.enable_to_work_time)
                self.get_fish()
                self.reset_all_condition()
                if self.reach_max_fising_count():
                    break
            except Exception as e:
                FishingLogger.error(traceback.format_exc())
            time.sleep(self.rest_time)

    def start_fishing(self):
        if self.is_foreground:
            if not self.is_wow_foreground_window():
                time.sleep(5)
            # bind fish skill to main ```action-bar``` number 1
            pyautogui.press('1')
        else:
            win32gui.PostMessage(self.wow_window, win32con.WM_KEYDOWN, self.fish_key, 0)
            win32gui.PostMessage(self.wow_window, win32con.WM_KEYUP, self.fish_key, 0)
        self.start_fishing_time = time.time()
        time.sleep(3) # sleep for a while to find fish_float
        self.find_fish_float()

    def is_bite_hook(self):
        cur_img = self.capture_main_fishing_screen()
        cur_contour = self.get_frame_contours(cur_img)
        cur_area = cv2.contourArea(cur_contour)
        if self.use_area:
            FishingLogger.info(
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
                FishingLogger.info(
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

    # (low_hsv, hight_hsv) color need adjust during environment or weather changed.
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
        return c

    def capture_main_fishing_screen(self):
        with mss.mss() as sct:
            capture_info = {
                'left': int(self.capture_left),
                'top': int(self.capture_top),
                'width': int(self.capture_width),
                'height': int(self.capture_height),
                'mon': 0 # all monitor
            }
            cur_screenshot = sct.grab(capture_info)
        #remember to convert data type
        #cur_captured_img = cv2.cvtColor(np.array(cur_screenshot), cv2.COLOR_RGB2BGR)
        cur_captured_img = np.array(cur_screenshot)
        return cur_captured_img

    def find_fish_float(self):
        cur_img = self.capture_main_fishing_screen()
        contour = self.get_frame_contours(cur_img)
        cur_moments = cv2.moments(contour)
        if cur_moments['m00'] != 0:
            self.fish_float_x = self.capture_left + int(cur_moments['m10'] / cur_moments['m00']) + self.float_offset
            self.fish_float_y = self.capture_top + int(cur_moments['m01'] / cur_moments['m00']) + self.float_offset

    def get_fish(self):
        if self.is_foreground:
            pyautogui.click(self.fish_float_x, self.fish_float_y)
            pyautogui.rightClick(self.fish_float_x, self.fish_float_y)
        else:
            win32gui.PostMessage(self.wow_window, win32con.WM_KEYDOWN, self.get_fish_key, 0)
            win32gui.PostMessage(self.wow_window, win32con.WM_KEYUP, self.get_fish_key, 0)

    def is_wow_foreground_window(self):
        return win32gui.GetForegroundWindow() == self.wow_window

    def cast_some_skill(self):
        if self.last_cast_time == 0 or time.time() - self.last_cast_time > self.cast_period:
            key_press_list = ['6']
            for key in key_press_list:
                self.send_key_to_wow(key)
            self.last_cast_time = time.time()
            time.sleep(self.enable_to_work_time)

    def random_jump(self):
        if util.roll_for_ratio(self.jump_ratio):
            self.send_key_to_wow('space')
            time.sleep(self.rest_time)

    def reach_max_fising_count(self):
        self.current_fishing_count += 1
        return self.current_fishing_count >= self.max_fishing_count

    def is_over_tolerate_time(self):
        return time.time() - self.start_fishing_time > self.tolerate_time

    def send_key_to_wow(self, key_board_str):
        real_key = \
            constant.key_board_map[key_board_str]['fg'] \
            if self.is_foreground \
            else constant.key_board_map[key_board_str]['bg']
        if self.is_foreground:
            pyautogui.press(real_key)
        else:
            win32gui.PostMessage(self.wow_window, win32con.WM_KEYDOWN, real_key, 0)
            win32gui.PostMessage(self.wow_window, win32con.WM_KEYUP, real_key, 0)
        time.sleep(self.rest_time)

    def test_capture(self):
        with mss.mss() as sct:
            capture_info = {
                'left': int(self.capture_left),
                'top': int(self.capture_top),
                'width': int(self.capture_width),
                'height': int(self.capture_height),
                'mon': 0 # all monitor
            }
            cur_screenshot = sct.grab(capture_info)
            return cur_screenshot

    def test(self):
        for i in range(0, 75):
            cur_img = self.test_capture()
            mss.tools.to_png(cur_img.rgb, cur_img.size, output='imgs/test_{}.png'.format(i))
            FishingLogger.info("Success capture screenshot, and save to path: {}".format('imgs/test_{}.png'.format(i)))
            time.sleep(1)