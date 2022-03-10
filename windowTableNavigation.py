# windowTableNavigation.py
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem

# Set up style sheet for the entire GUI
style_sheet = """
    QTableWidget {
        background-color: #E3E3E3;
        color: #393939;
        border-style: outset;
        gridline-color: #717171;

        selection-color: #393939;
        selection-background-color: #fffffd;
        border: 1px solid gray;
    }
"""


class TableNavigation(QTableWidget):
    def __init__(self, table_contact):
        super().__init__()
        self.table_contact = table_contact
        self.setupUI()
        self.setStyleSheet(style_sheet)

    def setupUI(self):
        self.setRowCount(13)
        self.setColumnCount(1)
        self.horizontalHeader().setVisible(False)
        self.verticalHeader().setVisible(False)
        # Запрещает изменять содержимое ячейки
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)
        # Установить таблицу как выделение целой строки
        self.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.setColumnWidth(0, 50)
        letters = ['АБ', 'ВГ', 'ДЕ', 'ЖЗИЙ', 'КЛ', 'МН', 'ОП', 'РС', 'ТУ', 'ФХ', 'ЦЧШЩ', 'ЪЫЬЭ', 'ЮЯ']
        for i, el in enumerate(letters):
            self.setRowHeight(i, 25)
            item = QTableWidgetItem(el)
            self.setItem(i, 0, item)
        self.setFixedSize(50, 327)
        self.cellClicked.connect(self.click_cell)

    def click_cell(self):
        row = self.currentRow()
        col = self.currentColumn()
        value = self.item(row, col)
        self.table_contact.nav_tableLetters = value.text()
        self.table_contact.setupUI()
