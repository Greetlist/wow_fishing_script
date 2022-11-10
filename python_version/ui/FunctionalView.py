from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout
from PySide6.QtWidgets import QGridLayout, QCheckBox, QFrame, QDoubleSpinBox
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
            'is_test': QCheckBox("Test Mode", self),
            'cast_periodically': QCheckBox("Random Cast", self),
            'use_coordinate': QCheckBox("Coordinate", self),
        }
        self.functional_value_input_dict = {
            'enable_to_work_time': (QLabel('StartToWorkTime: '), QDoubleSpinBox(self), 5.0),
            'rest_time': (QLabel('RestTime: '), QDoubleSpinBox(self), 1.0),
            'float_coordinate_changed_threshold': (QLabel('Threshold: '), QDoubleSpinBox(self), 40.0),
            'cast_period': (QLabel('Period: '), QDoubleSpinBox(self), 60.0),
        }
        col = 0
        for _, check_box in self.functional_check_box_dict.items():
            self.g_layout.addWidget(check_box, 0, col)
            col += 1
        row = 1
        for _, t in self.functional_value_input_dict.items():
            label, edit, default_value = t[0], t[1], t[2]
            label.setFrameShadow(QFrame.Raised)
            label.setBuddy(edit)
            #validator = QDoubleValidator(self)
            #edit.setValidator(validator)
            edit.setValue(default_value)
            edit.setMinimum(1.0)
            edit.setMaximum(3600.0)
            edit.setSingleStep(1.0)
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