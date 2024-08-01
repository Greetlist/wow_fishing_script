from PySide6.QtCore import QSize
from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PySide6.QtGui import QDoubleValidator

class DebugHSVColorView(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.edit_dict = {
            'min_list': dict(),
            'max_list': dict(),
        }
        self.init_button()
        self.init_child_widget()

    def init_button(self):
        self.debug_hsv_button = QPushButton("Debug HSV Color Range")
        self.debug_hsv_button.setCheckable(True)

    def init_child_widget(self):
        self.g_layout = QGridLayout()
        self.setLayout(self.g_layout)

        self.g_layout.addWidget(self.debug_hsv_button, 0, 0, 1, 4)
        row = 1
        for data_str, _ in self.edit_dict.items():
            cur_edit = QLineEdit(self)
            cur_label = QLabel(data_str + ':', self)
            cur_label.setBuddy(cur_edit)
            self.g_layout.addWidget(cur_label, row, 0)
            self.g_layout.addWidget(cur_edit, row, 2)
            row += 1
            self.edit_dict[data_str]['edit_instance'] = cur_edit
            self.edit_dict[data_str]['real_data'] = 0

    def set_edit_data(self, data_dict):
        for data_str, _ in self.edit_dict.items():
            self.edit_dict[data_str]['real_data'] = data_dict[data_str]
            self.edit_dict[data_str]['edit_instance'].setText(str(data_dict[data_str]))

    def set_click_function(self, func):
        self.debug_hsv_button.clicked.connect(func)

    def get_list(self):
        return self.edit_dict['min_list']['real_data'], self.edit_dict['max_list']['real_data']