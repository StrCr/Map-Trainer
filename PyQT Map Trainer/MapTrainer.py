import io
import sys
import sqlite3
import random

from PyQt6 import uic
from PyQt6.QtGui import QPixmap
from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout
from PyQt6 import QtCore, QtWidgets

from py_maptrainer import Ui_MainWindow

questions_dict = {1: "страны", 2: "столицы", 3: "регион", 4: "океан"}


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
        self.con = sqlite3.connect("map.sqlite")
        self.total_points = []
        self.answer_points = []

        self.game_btn.clicked.connect(self.start_game)
        self.game_btn.clicked.connect(self.next_game)
        self.game_answer_btn.clicked.connect(self.answer_game)
        self.game_next_btn.clicked.connect(self.next_game)
        self.result_btn.clicked.connect(self.end_game)

        # зона разработк
        self.layout = QVBoxLayout()
        self.scrollArea.setLayout(self.layout)

    def start_game(self):
        self.stackedWidget.setCurrentWidget(self.game_page)

    def answer_game(self):
        # доработать
        """self.answer_points = []
        if self.checkBox_2.isChecked():
            self.answer_points.append(100)"""

    def next_game(self):
        cur = self.con.cursor()
        random_id = random.randint(1, 4)
        print(random_id)
        cur.execute('SELECT maps_name FROM maps WHERE id=?', (random_id,))
        image_name = cur.fetchone()[0]
        print(image_name)
        pixmap = QPixmap(image_name)
        self.game_image.setPixmap(pixmap)
        self.game_image.setScaledContents(True)

        cur.execute('SELECT false_info_id FROM info WHERE id=?', (random_id,))
        question_ids = cur.fetchone()[0]
        if len(str(question_ids)) > 1:
            random_question_id = random.choice(question_ids.split(', '))
        else:
            random_question_id = question_ids
        question_text = questions_dict.get(int(random_question_id))
        self.game_question_label.setText(question_text)

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for i in range(2):
            new_check_box = QCheckBox("New Checkbox")
            self.layout.addWidget(new_check_box)

    def end_game(self):
        # доработать
        self.stackedWidget.setCurrentWidget(self.result_page)
        self.total_points.append(sum(self.answer_points))
        print(self.total_points)

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
    if hasattr(QtCore.Qt, 'AA_EnableHighDpiScaling'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_EnableHighDpiScaling, True)

    if hasattr(QtCore.Qt, 'AA_UseHighDpiPixmaps'):
        QtWidgets.QApplication.setAttribute(QtCore.Qt.AA_UseHighDpiPixmaps, True)

    app = QApplication(sys.argv)
    wnd = MapTrainer()
    wnd.show()
    sys.exception = except_hook
    sys.exit(app.exec())
