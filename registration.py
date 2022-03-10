# registration.py
import sys

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QMessageBox, QDateEdit, QApplication
from PyQt5.QtCore import Qt
from mariaDB_users import MariaDBUsers


class Registration(QWidget):
    def __init__(self):
        super().__init__()
        self.mariaUsers = MariaDBUsers()
        self.initializeUI()

    def initializeUI(self):
        """ Initialize thw window and display its contents to the screen (Registration) """
        self.setFixedSize(320, 260)
        self.setWindowTitle('Регистрация')
        self.setWindowModality(Qt.ApplicationModal)
        self.displayLineEdit()
        self.displayBirthCalendar()
        self.displayButton()

        with open("style.txt", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

        self.show()

    def displayLineEdit(self):
        """ Display Line Edit (user name, password, repeat password) """
        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText('Имя пользователя')
        self.user_name.resize(220, 30)
        self.user_name.move(50, 30)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText('Пароль')
        self.password.resize(220, 30)
        self.password.move(50, 75)
        self.password.setEchoMode(QLineEdit.Password)

        self.repeat_password = QLineEdit(self)
        self.repeat_password.setPlaceholderText('Повторите пароль')
        self.repeat_password.resize(220, 30)
        self.repeat_password.move(50, 120)
        self.repeat_password.setEchoMode(QLineEdit.Password)

    def displayBirthCalendar(self):
        """ Display Calendar (user name, password, repeat password) """
        self.birth_date = QDateEdit(self)
        self.birth_date.setDisplayFormat('yyyy-MM-dd')
        self.birth_date.resize(220, 30)
        self.birth_date.move(50, 165)

    def displayButton(self):
        """ Display Button (ok, cancel) """
        btn_ok = QPushButton("Ок", self)
        btn_ok.setObjectName("BtnGreen")
        btn_ok.resize(100, 25)
        btn_ok.move(50, 210)
        btn_ok.clicked.connect(self.event_btn_ok)

        btn_cancel = QPushButton("Отмена", self)
        btn_cancel.setObjectName("BtnRed")
        btn_cancel.resize(110, 25)
        btn_cancel.move(160, 210)
        btn_cancel.clicked.connect(self.event_btn_cancel)

    def event_btn_ok(self):
        """ Event close window registration and create new User """
        if self.password.text() != self.repeat_password.text():
            QMessageBox.warning(self, "Error Message", "Пароли не свопадают.", QMessageBox.Close)
        elif self.user_name.text() and self.password.text() and self.birth_date.text():
            self.mariaUsers.add(self.user_name.text(), self.password.text(), self.birth_date.text())
            self.close()
        else:
            QMessageBox.warning(self, "Error Message", "Заполните все поля.", QMessageBox.Close)

    def event_btn_cancel(self):
        """ Event close window registration"""
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            self.event_btn_ok()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    m = Registration()
    m.show()
    sys.exit(app.exec_())