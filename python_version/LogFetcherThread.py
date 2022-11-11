from PySide6.QtCore import QThread
from Logger import FishingLogger
import os
import time

class LogFetcherThread(QThread):
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget
        self.log_filename = os.path.join(FishingLogger.log_dir, FishingLogger.log_filename)
        self.file_fd = open(self.log_filename, 'a+')
        self.offset = 0

    def run(self):
        while True:
            new_text_line = self.read_log_text()
            self.parent_widget.append_text(new_text_line)
            time.sleep(1)

    def read_log_text(self):
        cur_state = os.stat(self.log_filename)
        if cur_state.st_size > self.offset:
            read_size = cur_state.st_size - self.offset
            new_text = self.file_fd.read(read_size)
            self.offset += read_size
            self.file_fd.seek(self.offset)
            return new_text
        return None