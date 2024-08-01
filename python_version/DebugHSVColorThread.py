from PySide6.QtCore import QThread

class DebugHSVColorThread(QThread):
    def __init__(self, fishing_helper, parent_widget, result_queue):
        super().__init__()
        self.fishing_helper = fishing_helper
        self.parent_widget = parent_widget
        self.result_queue = result_queue

    def run(self):
        min_list, max_list = self.fishing_helper.debug_hsv_color()
        self.result_queue.put(min_list)
        self.result_queue.put(max_list)