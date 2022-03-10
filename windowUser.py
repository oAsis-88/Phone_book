# windowUser.py
from datetime import datetime
import sys

from PyQt5.QtWidgets import QWidget, QPushButton, QMessageBox, QAction, QMainWindow, QVBoxLayout, QHBoxLayout, \
    QApplication, QMenu, QGridLayout, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter, QPen, QIcon, QPixmap, QPalette, QBrush

from mariaDB_contacts import MariaDBContacts
from windowAddUser import AddUser
from windowUpdateUser import UpdateUser
from windowTableNavigation import TableNavigation
from windowTableContacts import TableContacts
from notification import Notification

# Set up style sheet for the entire GUI
style_sheet = """
    #Navigation{
        background-color: #E3E3E3;
        border-width: 8px;
        border-style: solid;
        border-color: #E3E3E3;
    }
"""


class MainWindowUser(QMainWindow):
    def __init__(self, user):
        super().__init__()
        self.user = user
        self.maria_contacts = MariaDBContacts()
        self.initializeUI()
        self.setStyleSheet(style_sheet)

    def initializeUI(self):

        self.setFixedSize(555, 550)
        # self.setFixedSize(750, 700)
        # Убирает верхнюю полоску окна (название, свернуть/закрыть)
        self.setWindowFlags(Qt.FramelessWindowHint)
        self.setAttribute(Qt.WA_TranslucentBackground, True)
        self.setAttribute(Qt.WA_NoSystemBackground, True)

        # Инициализирует Окно пользователя
        self.displayWindow()
        # Инициализирует Окно с напоминанием об именинниках на ближайшую неделю
        self.notification()

        self.show()

    def displayWindow(self):
        """ Инициализирует Окно пользователя """
        self.layout = QGridLayout()
        self.layout.setSpacing(0)
        # self.layout.setContentsMargins(0, 0, 0, 0)

        # Инициализирует 2 Окна с навигацией и пользователем
        self.nav_acc()

        widget = QWidget()
        widget.setLayout(self.layout)
        self.setCentralWidget(widget)

    def notification(self):
        """ Инициализирует Окно с напоминанием об именинниках на ближайшую неделю """
        contacts_with_birth_on_next_week = self.maria_contacts.get_contacts_with_birth(self.user)
        if contacts_with_birth_on_next_week:
            self.notice = Notification(self.user, contacts_with_birth_on_next_week)
            # self.notification.show()

    def nav_acc(self):
        """ Инициализирует 2 Окна с навигацией и пользователем """
        self.account = QVBoxLayout()

        # Создает и заполняет Таблицу контактов
        self.tableContact = TableContacts(self.user, self.maria_contacts)
        self.tableContact.setupUI()

        # Создает Таблицу навигации для отображения контактов в Таблице контактов
        self.tableNavigation = TableNavigation(self.tableContact)

        # Создает Виджеты для взаимодействия с контактами
        self.create_account_Navigation()
        self.account.addWidget(self.tableContact)

        self.navigation = QVBoxLayout()
        self.navigation.addWidget(self.tableNavigation)
        self.layout.addLayout(self.navigation, 0, 0)
        self.layout.addLayout(self.account, 0, 1)


    def create_account_Navigation(self):
        """ Создает Виджеты для взаимодействия с контактами """
        navigation = QHBoxLayout()
        navigation.setSpacing(0)

        icon = QLabel()
        icon.setObjectName("Navigation")
        pixmap = QPixmap('user_icon.jpg')
        pixmap = pixmap.scaled(30, 30)
        icon.setPixmap(pixmap)

        user_status = QLabel('Зашли как <a href="#">Администратор</a>', self)
        user_status.setObjectName("Navigation")
        # user_status.linkActivated.connect(self.event_user_status)

        exit_acc = QLabel('<a href="#">выйти</a>')
        exit_acc.setObjectName("Navigation")
        exit_acc.linkActivated.connect(self.event_exit_acc)

        navigation.addWidget(icon)
        navigation.addWidget(user_status, Qt.AlignRight)
        navigation.addWidget(exit_acc)

        self.account.addLayout(navigation)

    def event_exit_acc(self):
        """ Действие осуществляет выход из аккаунта с закрытием программы"""
        # выход из программы с последующей авторизацией
        with open("cookie.txt", "w") as cookie:
            cookie.write('')
        self.close()


    def paintEvent(self, event=None):
        painter = QPainter(self)
        painter.setOpacity(0.5)
        painter.setBrush(Qt.gray)
        painter.setPen(QPen(Qt.white))
        painter.drawRect(self.rect())

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            self.event_ok()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = MainWindowUser(str('oasis'))
    m.show()
    sys.exit(app.exec_())
