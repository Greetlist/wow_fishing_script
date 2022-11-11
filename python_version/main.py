from ui import MainView
from PySide6.QtWidgets import QApplication
import argh
import sys

def run():
    app = QApplication(sys.argv)
    gui = MainView.MainView()
    gui.resize_and_show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    argh.dispatch_command(run)