import sys
import sqlite3
import random

from PyQt6 import QtCore, QtWidgets
from PyQt6.QtCore import QTimer
from PyQt6.QtGui import QPixmap, QImage
from PyQt6.QtWidgets import QApplication, QMainWindow, QCheckBox, QVBoxLayout, QRadioButton, QMessageBox

from py_maptrainer import Ui_MainWindow

questions_dict = {1: "Какая(-ие) страна(-ы) изображена(-ы) на карте?",
                  2: "Какая(-ие) столица(-ы) изображена(-ы) на карте?",
                  3: "Какой регион изображен на карте?",
                  4: "Какое море изображено на карте?"}
COLUMNS = ['countries', 'capitals', 'regions', 'seas']

# ToDo: использовать rows[0][1] для данных из таблицы
# ToDo: улучшить код


class MapTrainer(QMainWindow, Ui_MainWindow):
    def __init__(self):
        super().__init__()
        # uic.loadUi('ui_maptrainer5.ui', self)
        self.setupUi(self)

        self.layout = QVBoxLayout()
        self.scrollArea.setLayout(self.layout)

        """Перелистывание страниц виджетом QStackedWidget"""
        self.stackedWidget.setCurrentWidget(self.menu_page)

        self.menu_btn.clicked.connect(self.show_page)
        self.start_btn.clicked.connect(self.show_page)
        self.records_btn.clicked.connect(self.show_page)
        self.game_btn.clicked.connect(self.show_page)

        """Игра"""
        self.con = sqlite3.connect("map.sqlite")
        self.cur = self.con.cursor()
        self.cur.execute('SELECT COUNT(*) AS id FROM maps;')
        self.maps_id = self.cur.fetchone()[0]

        self.name = 0
        self.correct_answer = None
        self.false_answer = None
        self.answer_is_difficult = None
        self.game_has_started = False
        self.points = 0
        self.total_points = 0
        self.checkboxes = []
        self.radio_btns = []

        self.timer = QTimer(self)
        self.timer.setInterval(1000)
        self.timer.timeout.connect(self.update_timer)
        self.time_left = 150
        self.time_total = 0

        self.game_btn.clicked.connect(self.start_countdown)
        self.game_btn.clicked.connect(self.next_game)
        self.game_answer_btn.clicked.connect(self.answer_game)
        self.game_next_btn.clicked.connect(self.next_game)
        self.result_btn.clicked.connect(self.end_game)

    def start_countdown(self):
        self.timer.start()

    def update_timer(self):
        self.time_left -= 1
        minutes = self.time_left // 60
        seconds = self.time_left % 60
        self.game_timer.setText(f"Время: {minutes:02}:{seconds:02}")

        if self.time_left <= 0:
            self.timer.stop()
            self.end_game()

    def answer_game(self):
        correct_answers = 0
        incorrect_answers = 0
        self.time_total = 0
        """Подсчет очков для сложного вопроса"""
        if self.answer_is_difficult:
            for checkbox in self.checkboxes:
                if checkbox.text() in self.correct_answer and checkbox.isChecked():
                    correct_answers += 1
                if checkbox.text() in self.false_answer and checkbox.isChecked():
                    incorrect_answers += 1
            if correct_answers > incorrect_answers:
                self.time_total = (correct_answers - incorrect_answers) * 15
            if correct_answers < incorrect_answers:
                self.time_total = (incorrect_answers - correct_answers) * -10
            else:
                self.time_total = 5
        """Подсчет очков для простого вопроса"""
        if not self.answer_is_difficult:
            for radio_btn in self.radio_btns:
                if radio_btn.text() in self.correct_answer and radio_btn.isChecked():
                    correct_answers = 1
            if correct_answers == 1:
                self.time_total = 15
            else:
                self.time_total = -15

        self.points += correct_answers * 100

    def next_game(self):
        self.game_has_started = True
        self.name = self.start_name.text()
        self.menu_name.setText(self.name)

        self.time_left += self.time_total
        if self.time_total == 0:
            self.time_left -= 10
        self.total_points += self.points
        self.time_total = 0
        random_id = random.randint(1, self.maps_id)

        """Генерация изображения"""
        self.cur.execute(f'SELECT maps_name FROM maps WHERE id = {random_id};')
        image_name = self.cur.fetchone()[0]
        print(image_name)
        map_game = QImage(f'maps/{image_name}')
        self.game_image.setPixmap(QPixmap.fromImage(map_game))

        """Генерация вопроса"""
        self.cur.execute(f'SELECT false_info_id FROM info WHERE id = {random_id};')
        question_ids = self.cur.fetchone()[0]
        if len(str(question_ids)) > 1:
            random_question_id = random.choice(question_ids.split(', '))
        else:
            random_question_id = question_ids
        self.game_question_label.setText(questions_dict.get(int(random_question_id)))

        """Генерация вариантов ответа"""
        all_answers = []
        column = COLUMNS[int(random_question_id) - 1]

        self.cur.execute(f"SELECT {column} FROM info WHERE id = {random_id};")
        self.correct_answer = self.cur.fetchone()[0].split(', ')
        if len(self.correct_answer) > 1:
            self.correct_answer = random.sample(self.correct_answer, 2)
        all_answers += self.correct_answer

        self.cur.execute(f"SELECT {column} FROM false_info;")
        false_info = self.cur.fetchall()
        false_info = [i[0] for i in false_info]
        if len(self.correct_answer) > 1:
            self.false_answer = random.sample(false_info, 4)
            self.answer_is_difficult = True
        else:
            self.false_answer = random.sample(false_info, 3)
            self.answer_is_difficult = False
        all_answers += self.false_answer
        random.shuffle(all_answers)

        for i in reversed(range(self.layout.count())):
            self.layout.itemAt(i).widget().setParent(None)

        if self.answer_is_difficult:
            for answer in all_answers:
                checkbox = QCheckBox(answer)
                self.layout.addWidget(checkbox)
                self.checkboxes.append(checkbox)
        if not self.answer_is_difficult:
            for answer in all_answers:
                radio_btn = QRadioButton(answer)
                self.layout.addWidget(radio_btn)
                self.radio_btns.append(radio_btn)

    def end_game(self):
        self.timer.stop()
        self.time_left = 150
        self.stackedWidget.setCurrentWidget(self.result_page)
        self.result_name_label.setText(f"Пользователем {self.name}")
        self.result_points_label.setText(f"набрано {self.points} очков!")
        if self.points != 0:
            self.cur.execute('''INSERT INTO records (name, points) VALUES (?, ?)''', (self.name, self.points))
            self.con.commit()
        self.points = 0
        self.game_has_started = False

    def show_page(self):
        """Перелистывание страниц виджетом QStackedWidget"""
        sender = self.sender()
        if sender == self.menu_btn:
            if self.game_has_started:
                self.game_has_started = False
                answer = QMessageBox.question(self, "Подтверждение", f"Дествительно ли вы хотите выйти в главное меню",
                                              QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No,
                                              QMessageBox.StandardButton.No)
                if answer == QMessageBox.StandardButton.Yes:
                    self.stackedWidget.setCurrentWidget(self.menu_page)
            else:
                self.stackedWidget.setCurrentWidget(self.menu_page)
        if sender == self.start_btn:
            self.stackedWidget.setCurrentWidget(self.start_settings_page)
        if sender == self.records_btn:
            self.records_list.clear()
            self.cur.execute('''SELECT name, points FROM records ORDER BY points DESC''')
            records = self.cur.fetchall()
            for record in records:
                record_name, record_points = record
                if record_name:
                    self.records_list.addItem(f'{record_name}.....{record_points}{'.' * 500}')
                else:
                    self.records_list.addItem(f'Player.....{record_points}{'.' * 500}')
            self.stackedWidget.setCurrentWidget(self.records_page)
        if sender == self.game_btn:
            self.stackedWidget.setCurrentWidget(self.game_page)


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
