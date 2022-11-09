from PySide6.QtCore import QThread

class FishingThread(QThread):
    def __init__(self, fishing_helper):
        super().__init__()
        self.fishing_helper = fishing_helper

    def run(self):
        self.fishing_helper.start()