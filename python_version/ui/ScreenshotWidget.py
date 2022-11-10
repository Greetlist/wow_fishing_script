from PySide6.QtCore import QSize, Qt, QRect
from PySide6.QtWidgets import QWidget, QMenu
from PySide6.QtGui import QPixmap, QGuiApplication
from PySide6.QtGui import QPainter, QColor, QPen
from PySide6.QtGui import QCursor, QAction, QIcon
import os

class ScreenShotMainWidget(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.parent = parent
        self.capture_total_screen()
        self.init_window()
        self.init_screenshot_menu()
        self.mouse_press = False
        self.is_cancel = False

    def capture_total_screen(self):
        total_screens = QGuiApplication.screens() #main screen's index is 0
        self.max_height = 0
        self.total_width = 0
        for screen in total_screens:
            screen_rect = screen.geometry()
            self.max_height = max(self.max_height, screen_rect.height())
            self.total_width += screen_rect.width()

        cur_pixmap = QPixmap(QSize(self.total_width, self.max_height))
        painter = QPainter(cur_pixmap)
        blank_color = QColor(0, 0, 0, 0)
        painter.fillRect(cur_pixmap.rect(), blank_color)
        for screen in total_screens:
            screen_pixmap = screen.grabWindow(0)
            screen_rect = screen.geometry()
            painter.drawPixmap(screen_rect, screen_pixmap)
        painter.end()
        self.origin_pixmap = cur_pixmap

    def init_window(self):
        self.setMouseTracking(True)
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint)
        self.setWindowState(Qt.WindowActive | Qt.WindowFullScreen)

    def init_screenshot_menu(self):
        self.menu = QMenu(self)
        static_img_path = os.path.join(os.path.dirname(__file__), 'static')
        confirm_action = QAction(QIcon('{}/confirm.png'.format(static_img_path)), "Confirm", self)
        confirm_action.setCheckable(True)
        confirm_action.triggered.connect(self.finish_screenshot)
        cancel_action = QAction(QIcon('{}/cancel.png'.format(static_img_path)), "Cancel", self)
        cancel_action.setCheckable(True)
        cancel_action.triggered.connect(self.cancel_screenshot)
        self.menu.addAction(confirm_action)
        self.menu.addAction(cancel_action)

    def paintEvent(self, e):
        painter = QPainter(self)
        shadow_color = QColor(0, 0, 0, 100)
        pen = QPen(QColor(255, 0, 0, 255), 3, Qt.SolidLine, Qt.SquareCap)
        painter.setPen((pen))

        painter.drawPixmap(self.origin_pixmap.rect(), self.origin_pixmap)
        painter.fillRect(self.origin_pixmap.rect(), shadow_color)

        if (self.mouse_press):
            left, top, right, bottom = self.calc_real_rect()
            cur_rect = QRect(left, top, right - left, bottom - top)
            cur_captured_pixmap = self.origin_pixmap.copy(cur_rect)
            painter.drawPixmap(cur_rect.topLeft(), cur_captured_pixmap)
            painter.drawRect(cur_rect)
            pen.setColor(QColor(255, 255, 255, 255))
            painter.setPen(pen)
            painter.drawText(
                left + 2, top - 5, 
                "{} X {}".format(right - left, bottom - top)
            )
        painter.end()

    def calc_real_rect(self):
        real_left = self.start_x if self.start_x < self.end_x else self.end_x
        real_top = self.start_y if self.start_y < self.end_y else self.end_y
        real_right = self.end_x if self.start_x < self.end_x else self.start_x
        real_bottom = self.end_y if self.start_y < self.end_y else self.start_y
        return real_left, real_top, real_right, real_bottom

    def keyPressEvent(self, e):
        if (e.key() == Qt.Key_Escape):
            print('Press Escape, Close')
            self.cancel_screenshot()

    def cancel_screenshot(self):
        self.is_cancel = True
        self.close()

    def mousePressEvent(self, e):
        self.mouse_press = True
        self.start_x = e.globalPosition().x()
        self.start_y = e.globalPosition().y()

    def mouseReleaseEvent(self, e):
        self.mouse_press = False
        self.menu.exec(QCursor.pos())

    def mouseMoveEvent(self, e):
        if self.mouse_press:
            self.end_x = e.globalPosition().x()
            self.end_y = e.globalPosition().y()
            self.update() #force invoke painterEvent

    def finish_screenshot(self):
        left, top, right, bottom = self.calc_real_rect()
        print('left: {left}, top: {top}, right: {right}, bottom: {bottom}'.format(**locals()))
        self.close()

    def get_captured_pixmap_rect(self):
        left, top, right, bottom = self.calc_real_rect()
        return {
            'left': left,
            'top': top,
            'right': right,
            'bottom': bottom,
            'width': right - left,
            'height': bottom - top,
        }

    def closeEvent(self, e):
        if not self.is_cancel:
            self.parent.set_edit_data(self.get_captured_pixmap_rect())