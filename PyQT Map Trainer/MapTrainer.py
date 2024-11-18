import io
import sys

from PyQt6 import uic
from PyQt6.QtWidgets import QApplication, QMainWindow

from py_maptrainer import Ui_MainWindow


class MapTrainer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('example.ui', self)
        self.setupUi(self)

    def example(self):
        pass


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MapTrainer()
    wnd.show()
    sys.exception = except_hook
    sys.exit(app.exec())
