from PySide6.QtWidgets import QWidget, QLineEdit, QLabel, QGridLayout
from PySide6.QtWidgets import QGridLayout, QCheckBox, QFrame, QDoubleSpinBox
from PySide6.QtCore import Qt

class FunctionalView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_child_widget()

    def init_child_widget(self):
        self.g_layout = QGridLayout()
        self.setLayout(self.g_layout)
        self.init_check_boxs()
        self.init_config_input()

    def init_check_boxs(self):
        self.functional_check_box_dict = {
            'is_test': (QCheckBox("Test Mode", self), 1, 0),
            'is_cast_periodically': (QCheckBox("Random Cast", self), 1, 1),
            'is_foreground': (QCheckBox("Running Mode", self), 2, 0),
            'use_coordinate': (QCheckBox("Coordinate", self), 2, 1),
        }
        for _, check_box_info in self.functional_check_box_dict.items():
            check_box, row, col = check_box_info[0], check_box_info[1], check_box_info[2]
            self.g_layout.addWidget(check_box, row, col)
    
    def init_config_input(self):
        self.functional_value_input_dict = {
            'wow_window_name':  (QLabel('Wow Window Name: '), QLineEdit(self), "魔兽世界", 3),
            'enable_to_work_time': (QLabel('StartToWorkTime(s): '), QDoubleSpinBox(self), 5.0, 4),
            'rest_time': (QLabel('RestTime(s): '), QDoubleSpinBox(self), 1.0, 5),
            'float_coordinate_changed_threshold': (QLabel('Threshold(s): '), QDoubleSpinBox(self), 40.0, 6),
            'cast_period': (QLabel('Cast Period(s): '), QDoubleSpinBox(self), 60.0, 7),
        }
        for _, t in self.functional_value_input_dict.items():
            label, edit, default_value, row = t[0], t[1], t[2], t[3]
            label.setFrameShadow(QFrame.Raised)
            label.setBuddy(edit)
            if type(edit) == QLineEdit:
                edit.setText(default_value)
            else:
                edit.setValue(default_value)
                edit.setMinimum(1.0)
                edit.setMaximum(3600.0)
                edit.setSingleStep(1.0)
            self.g_layout.addWidget(label, row, 0)
            self.g_layout.addWidget(edit, row, 1)

    def get_all_config_data(self):
        res = {}
        for config_name, check_box_tuple in self.functional_check_box_dict.items():
            check_box = check_box_tuple[0]
            res[config_name] = check_box.checkState() == Qt.Checked
        for config_name, t in self.functional_value_input_dict.items():
            edit = t[1]
            res[config_name] = edit.text() if type(edit) == QLineEdit else float(edit.text())
        return res