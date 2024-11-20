import sqlite3
con = sqlite3.connect('map.sqlite')
cur = con.cursor()
query = """SELECT maps_name FROM maps Where id = 1;"""
res = cur.execute(query)
con.commit()
con.close()
print(res)

""" self.pushButton.clicked.connect(self.start)
    self.saveButton.clicked.connect(self.save)
    self.con = sqlite3.connect("films_db.sqlite")

def save(self):
    row_selected = self.tableWidget.currentRow()
    data = [self.tableWidget.item(row_selected, i).text() for i in range(self.tableWidget.columnCount())]
    data[1] = data[1][::-1]
    data[2] = str(int(data[2]) + 1000)
    data[4] = str(int(data[4]) * 2)
    id = data[0]
    answer = QMessageBox.question(self, "python", f"Дествительно заменить эелементы с id {id}",
                                  QMessageBox.Yes, QMessageBox.No)
    if answer == QMessageBox.Yes:
        cur = self.con.cursor()
        query = f"DELETE FROM films WHERE id = {id}"
        cur.execute(query)
        query = "INSERT INTO films WHERE VALUES (?,?,?,?,?)"
        cur.execute(query, data)
        self.con.commit()

def start(self):
    try:
        cur = self.con.cursor()
        query = "SELECT * FROM films WHERE" + self.textEdit.toPlainText()
        res = cur.execute(query).fetchall()
        if res:
            self.tableWidget.setRowCount(len(res))
            self.tableWidget.setColumnCount(len(res[0]))
            for i, row in enumerate(res):
                for j, item in enumerate(row):
                    self.tableWidget.setItem(i, j, QTableWidgetItem(str(item)))
            self.statusBar().showMessage("")
        else:
            self.statusBar().showMessage("По этому запросу ничего не найдено")
    except Exception:
        self.statusBar().showMessage("По этому запросу ничего не найдено")"""