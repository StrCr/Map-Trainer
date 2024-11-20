import io
import sys
import sqlite3

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow

from py_maptrainer import Ui_MainWindow


class MapTrainer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('ui_maptrainer2.ui', self)
        self.setupUi(self)

        # кнопки для переключения страниц
        self.stackedWidget.setCurrentWidget(self.menu_page)

        self.menu_btn.clicked.connect(self.show_page)
        self.start_btn.clicked.connect(self.show_page)
        self.records_btn.clicked.connect(self.show_page)
        self.settings_btn.clicked.connect(self.show_page)
        self.achievements_btn.clicked.connect(self.show_page)
        # self.buttonGroup.buttonClicked.connect(self.show_page)

        # игровая зона
        self.game_btn.clicked.connect(self.start_game)
        self.result_btn.clicked.connect(self.end_game)

        # зона разработки
        self.pixmap = QPixmap('caspian_sea.jpg')
        self.game_image.setPixmap(self.pixmap)
        self.game_image.setScaledContents(True)

    def start_game(self):
        self.stackedWidget.setCurrentWidget(self.game_page)

    def end_game(self):
        self.stackedWidget.setCurrentWidget(self.result_page)

    def show_page(self):
        sender = self.sender()
        # Попытаться сократить еще больше с использованием словаря
        if sender == self.menu_btn:
            self.stackedWidget.setCurrentWidget(self.menu_page)
        if sender == self.start_btn:
            self.stackedWidget.setCurrentWidget(self.start_settings_page)
        if sender == self.records_btn:
            self.stackedWidget.setCurrentWidget(self.records_page)
        if sender == self.settings_btn:
            self.stackedWidget.setCurrentWidget(self.settings_page)
        if sender == self.achievements_btn:
            self.stackedWidget.setCurrentWidget(self.achievements_page)


def except_hook(cls, exception, traceback):
    sys.__excepthook__(cls, exception, traceback)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    wnd = MapTrainer()
    wnd.show()
    sys.exception = except_hook
    sys.exit(app.exec())
