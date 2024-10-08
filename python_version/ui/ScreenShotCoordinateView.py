from ui import ScreenShotWidget
from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PySide6.QtGui import QDoubleValidator

class ScreenShotCoordinateView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.monitor_dict = {
            'monitor_width': {
                'function': self.on_monitor_width_changed,
                'value': 1920,
                'widget': None
            },
            'monitor_height': {
                'function': self.on_monitor_height_changed,
                'value': 1080,
                'widget': None
            }
        }
        self.edit_dict = {
            'left': dict(),
            'top': dict(),
            'right': dict(),
            'bottom': dict(),
            'width': dict(),
            'height': dict(),
        }
        self.init_button()
        self.init_child_widget()

    def init_button(self):
        self.rect_button = QPushButton("Get Fish Area")
        self.rect_button.setCheckable(True)
        self.rect_button.clicked.connect(self.show_screenshot_dialog)

    def show_screenshot_dialog(self):
        widget = ScreenShotWidget.ScreenShotMainWidget(
            self, 
            self.monitor_dict['monitor_width']['value'],
            self.monitor_dict['monitor_height']['value']
        )
        widget.show()
        widget.setFixedSize(QSize(widget.total_width, widget.max_height)) #must invoke after show() function.

    def init_child_widget(self):
        self.g_layout = QGridLayout()
        self.setLayout(self.g_layout)

        self.g_layout.addWidget(self.rect_button, 0, 0, 1, 4)
        row = 1
        for data_str, info in self.monitor_dict.items():
            cur_edit = QLineEdit(self)
            cur_label = QLabel(data_str + ':', self)
            validator = QDoubleValidator(self)
            cur_edit.setValidator(validator)
            cur_edit.textChanged.connect(self.monitor_dict[data_str]['function'])
            self.monitor_dict[data_str]['widget'] = cur_edit
            cur_label.setBuddy(cur_edit)
            self.g_layout.addWidget(cur_label, row, 0)
            self.g_layout.addWidget(cur_edit, row, 1)
            row += 1
            cur_edit.setText(str(info['value']))

        self.g_layout.addWidget
        for data_str, _ in self.edit_dict.items():
            cur_edit = QLineEdit(self)
            cur_label = QLabel(data_str + ':', self)
            cur_label.setBuddy(cur_edit)
            validator = QDoubleValidator(self)
            cur_edit.setValidator(validator)
            self.g_layout.addWidget(cur_label, row, 0)
            self.g_layout.addWidget(cur_edit, row, 1)
            row += 1
            self.edit_dict[data_str]['edit_instance'] = cur_edit
            self.edit_dict[data_str]['real_data'] = 0

    def set_edit_data(self, data_dict):
        for data_str, _ in self.edit_dict.items():
            self.edit_dict[data_str]['real_data'] = data_dict[data_str]
            self.edit_dict[data_str]['edit_instance'].setText(str(data_dict[data_str]))

    def set_monitor_index_data(self, data_dict):
        self.monitor_data = data_dict
    
    def get_monitor_index_data(self):
        return self.monitor_data

    def get_capture_coordinate(self):
        res = {}
        for data_str, _ in self.edit_dict.items():
            res[data_str] = self.edit_dict[data_str]['real_data']
        return res

    def on_monitor_width_changed(self):
        if self.monitor_dict['monitor_width']['widget'].text() != '':
            self.monitor_dict['monitor_width']['value'] = float(self.monitor_dict['monitor_width']['widget'].text())
        else:
            self.monitor_dict['monitor_width']['value'] = 1920

    def on_monitor_height_changed(self):
        if self.monitor_dict['monitor_height']['widget'].text():
            self.monitor_dict['monitor_height']['value'] = float(self.monitor_dict['monitor_height']['widget'].text())
        else:
            self.monitor_dict['monitor_height']['value'] = 1080
