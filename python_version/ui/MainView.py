
from PySide6.QtWidgets import QWidget, QPushButton, QGridLayout
from threading import Thread

class MainView(QWidget):
    def __init__(self, parent=None):
        super().__init__()
        self.init_child_widget()

    def init_child_widget(self):
        self.screeshot_view = ScreenShotCoordinateView(self)
        self.functional_view = FunctionalView(self)

        self.start_button = QPushButton("Start Fishing")
        self.start_button.setCheckable(True)
        self.start_button.clicked.connect(self.start_fishing)

        self.stop_button = QPushButton("Stop")
        self.stop_button.setCheckable(True)
        self.stop_button.clicked.connect(self.stop_fishing)

        self.g_layout = QGridLayout()
        self.setLayout(self.g_layout)
        self.g_layout.addWidget(self.screeshot_view, 0, 0)
        self.g_layout.addWidget(self.functional_view, 0, 1)
        self.g_layout.addWidget(self.start_button, 1, 0)
        self.g_layout.addWidget(self.stop_button, 1, 1)

    def start_fishing(self):
        functional_config = self.functional_view.get_all_config_data()
        capture_area_coordinate = self.screeshot_view.get_capture_coordinate()
        self.fishing_instance = FishingHelper(functional_config, capture_area_coordinate)
        running_thread = Thread(self.fishing_instance.start())
        running_thread.start()

    def stop_fishing(self):
        self.fishing_instance.stop()

    def resize_and_show(self):
        self.show()
        self.setFixedSize(QSize(500, 400))