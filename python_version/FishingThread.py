from PySide6.QtCore import QThread

class FishingThread(QThread):
    def __init__(self, fishing_helper, parent_widget):
        super().__init__()
        self.fishing_helper = fishing_helper
        self.parent_widget = parent_widget

    def run(self):
        if self.fishing_helper.is_test:
            self.fishing_helper.test()
        else:
            self.fishing_helper.start()
        self.parent_widget.reset_fishing_button()