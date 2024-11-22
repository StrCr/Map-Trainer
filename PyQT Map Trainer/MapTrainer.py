import io
import sys
import sqlite3
import random

from PyQt6 import uic
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QScrollArea, QStackedWidget
from PyQt6 import QtCore, QtWidgets

from py_maptrainer import Ui_MainWindow

questions_dict = {1: "страны", 2: "столицы", 3: "регион", 4: "океан"}


class MapTrainer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('ui_maptrainer2.ui', self)
        self.setupUi(self)

        # кнопки для перелистывания страниц
        self.stackedWidget.setCurrentWidget(self.menu_page)

        self.menu_btn.clicked.connect(self.show_page)
        self.start_btn.clicked.connect(self.show_page)
        self.records_btn.clicked.connect(self.show_page)
        self.settings_btn.clicked.connect(self.show_page)
        self.achievements_btn.clicked.connect(self.show_page)
        # self.buttonGroup.buttonClicked.connect(self.show_page)

        # игровая зона
        self.con = sqlite3.connect("map.sqlite")
        self.cur = self.con.cursor()

        self.game_btn.clicked.connect(self.start_game)
        self.game_btn.clicked.connect(self.next_game)
        self.game_answer_btn.clicked.connect(self.answer_game)
        self.game_next_btn.clicked.connect(self.next_game)
        self.result_btn.clicked.connect(self.end_game)

        # зона разработк
        self.checkboxes = []
        self.layout = QVBoxLayout()
        self.scrollArea.setLayout(self.layout)

    def start_game(self):
        self.stackedWidget.setCurrentWidget(self.game_page)

    def answer_game(self):
        correct = 0
        incorrect = 0
        for checkbox in self.checkboxes:
            if checkbox.text() in self.correct_answer and checkbox.isChecked():
                correct += 1
            if checkbox.text() in self.false_answer and checkbox.isChecked():
                incorrect += 1
        print(correct, incorrect)

    def next_game(self):
        random_id = random.randint(1, 4)

        # генерация изображения
        self.cur.execute('SELECT maps_name FROM maps WHERE id=?', (random_id,))
        image_name = self.cur.fetchone()[0]
        map_game = QImage(image_name)
        self.game_image.setPixmap(QPixmap.fromImage(map_game))

        # генерация вопроса
        self.cur.execute('SELECT false_info_id FROM info WHERE id=?', (random_id,))
        question_ids = self.cur.fetchone()[0]
        if len(str(question_ids)) > 1:
            random_question_id = random.choice(question_ids.split(', '))
        else:
            random_question_id = question_ids
        question_text = questions_dict.get(int(random_question_id))
        self.game_question_label.setText(f"Какой(-ие) {question_text} представлен(-ы) на карте?")

        # генерация вариантов ответа
        all_answers = []
        columns = ['countries', 'capitals', 'regions', 'seas']
        column = columns[int(random_question_id) - 1]
        self.cur.execute(f"SELECT {column} FROM info WHERE id = {random_id}")
        self.correct_answer = self.cur.fetchone()[0].split(', ')
        if len(self.correct_answer) > 1:
            self.correct_answer = random.sample(self.correct_answer, 2)
        all_answers += self.correct_answer

        self.cur.execute(f"SELECT {column} FROM false_info")
        false_info = self.cur.fetchall()
        false_info = [i[0] for i in false_info]
        if len(self.correct_answer) > 1:
            self.false_answer = random.sample(false_info, 4)
        else:
            self.false_answer = random.sample(false_info, 3)
        all_answers += self.false_answer
        random.shuffle(all_answers)

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        for answer in all_answers:
            checkbox = QCheckBox(answer)
            self.layout.addWidget(checkbox)
            self.checkboxes.append(checkbox)

        """      
        self.cur.execute(f"SELECT * FROM false_info WHERE {self.getColumnName()} "
                         f"= (SELECT {self.getColumnName()} FROM info WHERE id = {self.current_id})")
        row = self.cur.fetchone()self.cur.execute(f"SELECT * FROM false_info WHERE {self.getColumnName()} "
                         f"= (SELECT {self.getColumnName()} FROM info WHERE id = {self.current_id})")
        row = self.cur.fetchone()"""

    def end_game(self):
        # доработать
        self.stackedWidget.setCurrentWidget(self.result_page)
        self.total_points.append(sum(self.answer_points))
        print(self.total_points)

    def show_page(self):
        # перелистывание страниц виджетом QStackedWidget
        sender = self.sender()
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
