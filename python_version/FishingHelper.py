import win32gui
import win32con
import pyautogui
import time
import cv2
import numpy as np

class FishingHelper:
    def __init__(self, functional_config, capture_area_coordinate) -> None:
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

        self.init_functional_config(functional_config)
        self.init_capture_area(capture_area_coordinate)

    def init_key_binding(self):
        self.fish_key = 0x31 #key_board 1
        self.get_fish_key = 0x32 #key_board 2
        self.skill_1 = 0x37 #key_board 7
        self.skill_2 = 0x38 #key_board 8
        self.skill_3 = 0x39 #key_board 9

    def init_functional_config(self, functional_config):
        self.wow_window_name = functional_config['wow_window_name'] # need to be utf-8
        self.wow_window = None
        self.use_coordinate = functional_config['use_coordinate']
        self.use_area = not self.use_coordinate
        self.enable_to_work_time = functional_config['enable_to_work_time']  # unit: second
        self.rest_time = functional_config['enable_to_work_time'] # unit: second
        self.float_area_changed_threshold = 45
        self.float_coordinate_changed_threshold = float(functional_config['float_coordinate_changed_threshold'])
        self.cast_period = functional_config['cast_period'] # unit: second
        self.is_cast_periodically = functional_config['is_cast_periodically'] # unit: second
        self.is_test = functional_config['is_test']
        self.is_foreground = functional_config['is_foreground']

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
        return True

    def start(self):
        while True:
            if self.is_cast_periodically:
                self.cast_some_skill()
            self.start_fishing()
            while not self.is_over_tolerate_time() and not self.is_bite_hook():
                time.sleep(self.wait_bite_time)
            while not self.is_wow_foreground_window():
                time.sleep(self.enable_to_work_time)
            self.get_fish()
            self.reset_all_condition()
            time.sleep(self.rest_time)

    def start_fishing(self):
        if not self.is_wow_foreground_window():
            time.sleep(5)
        # bind fish skill to main ```action-bar``` number 1
        if self.is_foreground:
             pyautogui.press('1')
        else:
            win32gui.PostMessage(self.wow_window, win32con.WM_CHAR, self.fish_key, 0)
        self.start_fishing_time = time.time()
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

    # (low_hsv, hight_hsv) color need adjust during environment or weather changed.
    def get_frame_contours(self, frame_img):
        img_hsv = cv2.cvtColor(frame_img, cv2.COLOR_BGR2HSV)
        low_hsv = np.array([0, 65, 0])
        high_hsv = np.array([10, 255, 255])
        img_mask = cv2.inRange(img_hsv, low_hsv, high_hsv)
        img_morph = img_mask.copy()
        cv2.erode(img_morph, (3, 3), img_morph, iterations=2)
        cv2.dilate(img_morph, (3, 3), img_morph, iterations=2)
        cnts, _ = cv2.findContours(img_morph.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
        c = max(cnts, key=cv2.contourArea)
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
            self.fish_float_x = self.capture_left + int(cur_moments['m10'] / cur_moments['m00'])
            self.fish_float_y = self.capture_top + int(cur_moments['m01'] / cur_moments['m00'])

    def get_fish(self):
        if self.is_foreground:
            pyautogui.click(self.fish_float_x, self.fish_float_y)
            pyautogui.rightClick(self.fish_float_x, self.fish_float_y)
        else:
            win32gui.PostMessage(self.wow_window, win32con.WM_CHAR, self.get_fish_key, 0)

    def is_wow_foreground_window(self):
        return win32gui.GetForegroundWindow() == self.wow_window

    def cast_some_skill(self):
        if self.last_cast_time == 0 or time.time() - self.last_cast_time > self.cast_period:
            if self.is_foreground:
                pyautogui.press('6')
            else:
                win32gui.PostMessage(self.wow_window, win32con.WM_CHAR, self.skill_1, 0)
            self.last_cast_time = time.time()
            time.sleep(self.enable_to_work_time)

    def is_over_tolerate_time(self):
        return time.time() - self.start_fishing_time > self.tolerate_time

    def test_capture(self):
        main_screen_region = (
            self.capture_left,
            self.capture_top,
            self.capture_width,
            self.capture_height,
        )
        cur_screenshot = pyautogui.screenshot(region=main_screen_region)
        return cur_screenshot

    def test(self):
        for i in range(0, 75):
            cur_img = self.test_capture()
            cur_img.save('imgs/test_{}.png'.format(i))
            time.sleep(1)