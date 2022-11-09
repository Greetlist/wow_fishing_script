from PySide6.QtWidgets import QWidget, QPushButton, QLineEdit, QLabel, QGridLayout
from PySide6.QtWidgets import QGridLayout, QMenu, QCheckBox
from PySide6.QtGui import QDoubleValidator
from PySide6.QtCore import Qt

class FunctionalView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_child_widget()

    def init_child_widget(self):
        self.g_layout = QGridLayout()
        self.setLayout(self.g_layout)
        self.functional_check_box_dict = {
            #'is_test': QCheckBox("Test Mode", self),
            'cast_skill': QCheckBox("Cast Random", self),
            'use_coordinate': QCheckBox("Coordinate", self),
        }
        self.functional_value_input_dict = {
            'enable_to_work_time': (QLabel('StartToWorkTime: '), QLineEdit(self)),
            'rest_time': (QLabel('RestTime: '), QLineEdit(self)),
            'float_coordinate_changed_threshold': (QLabel('Threshold(x^2 + y^2): '), QLineEdit(self)),
            'cast_period': (QLabel('Period: '), QLineEdit(self)),
        }
        col = 0
        for _, check_box in self.functional_check_box_dict.items():
            self.g_layout.addWidget(check_box, 0, col)
            col += 1
        row = 1
        for _, t in self.functional_value_input_dict.items():
            label, edit = t[0], t[1]
            label.setBuddy(edit)
            validator = QDoubleValidator(self)
            edit.setValidator(validator)
            self.g_layout.addWidget(label, row, 0)
            self.g_layout.addWidget(edit, row, 1)
            row += 1

    def get_all_config_data(self):
        res = {}
        for config_name, check_box in self.functional_check_box_dict.items():
            res[config_name] = check_box.checkState() == Qt.Checked
        for config_name, t in self.functional_value_input_dict.items():
            edit = t[1]
            res[config_name] = float(edit.text())
        return res