# windowTableContacts.py
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTableWidget, QAbstractItemView, QTableWidgetItem, QMenu, QAction, QMessageBox

from windowAddUser import AddUser
from windowUpdateUser import UpdateUser

# Set up style sheet for the entire GUI
style_sheet = """
    QTableWidget {
        background-color: #E3E3E3;
        color: #393939;
        border-style: outset;
        gridline-color: #717171;

        selection-color: white;
        selection-background-color: #fffffd;
        border: 1px solid gray;
        alternate-background-color: #fffffd
    }
"""


class TableContacts(QTableWidget):
    def __init__(self, user=None, database=None, nav=None):
        super().__init__()
        self.user = user
        self.maria_contacts = database
        self.nav_tableLetters = nav
        self.setStyleSheet(style_sheet)

    def setupUI(self):
        """ Создает таблицу с отображением контактов """
        self.setRowCount(13)
        self.setColumnCount(3)

        # Убирает вертикальный заголовок
        self.verticalHeader().setVisible(False)

        # Удаляет вертикальную полосу прокрутки
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        # Растягивает колонки на всю ширину
        self.horizontalHeader().setStretchLastSection(True)
        self.setHorizontalHeaderLabels(["Имя", "телефон", "Дата рождения"])

        # Запрещает выделять ячейки
        self.setSelectionMode(QAbstractItemView.NoSelection)

        # Запрещает изменять содержимое ячейки
        self.setEditTriggers(QAbstractItemView.NoEditTriggers)

        # Установить таблицу как выделение целой строки
        self.setSelectionBehavior(QAbstractItemView.SelectRows)

        # Устанавливает свойство чередующихся цветов
        self.setAlternatingRowColors(True)

        # Получаем данные из базы данных и заполняем таблицу
        if self.nav_tableLetters:
            self.clearContents()
            tableData = self.maria_contacts.get_name_by_symbol(self.user, self.nav_tableLetters)
            if tableData:
                for i, (name, phone, birth) in enumerate(tableData):
                    self.setItem(i, 0, QTableWidgetItem(name))
                    self.setItem(i, 1, QTableWidgetItem(phone))
                    self.setItem(i, 2, QTableWidgetItem(birth))
            else:
                self.clearContents()

        self.setColumnWidth(0, 180)
        self.setColumnWidth(1, 180)

    def contextMenuEvent(self, event):
        """ Создает контекстное меню  """
        context_menu = QMenu(self)
        self.add_user = QAction("add user", self)
        self.add_user.triggered.connect(self._addUser)
        self.remove_user = QAction("remove user", self)
        self.remove_user.triggered.connect(self._removeUser)
        self.update_user = QAction("update user", self)
        self.update_user.triggered.connect(self._updateUser)
        context_menu.addAction(self.add_user)
        context_menu.addSeparator()
        context_menu.addAction(self.remove_user)
        context_menu.addSeparator()
        context_menu.addAction(self.update_user)
        context_menu.exec_(self.mapToGlobal(event.pos()))

    def _addUser(self):
        """ Инициализирует Окно с добавлением контакта """
        self.addUser = AddUser(self.user, self.maria_contacts, self)
        self.addUser.show()

    def _removeUser(self):
        """ Удаляет контакт """
        current_row = self.currentRow()
        if self.item(current_row, 0) is not None:
            name = self.item(current_row, 0).text()
            phone = self.item(current_row, 1).text()
            birth = self.item(current_row, 2).text()
            birth = datetime.strptime(birth, '%d-%m-%Y').strftime('%Y-%m-%d')
            self.maria_contacts.remove(self.user, name, phone, birth)
            self.clearContents()
            self.setupUI()
        else:
            QMessageBox.warning(self, "Error Message", "Выберете контакт.", QMessageBox.Close)

    def _updateUser(self):
        """ Инициализирует Окно с обновлением контакта """
        current_row = self.currentRow()
        if self.item(current_row, 0) is not None:
            name = self.item(current_row, 0).text()
            phone = self.item(current_row, 1).text()
            birth = self.item(current_row, 2).text()
            self.updateUser = UpdateUser(self.user, name, phone, birth, self.maria_contacts, self)
            self.updateUser.show()
        else:
            QMessageBox.warning(self, "Error Message", "Выберете контакт.", QMessageBox.Close)