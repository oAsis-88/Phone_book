# authorization.py

from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QCheckBox, QLabel, QMessageBox
from PyQt5.QtCore import Qt
from passwordRecovery import PasswordRecovery
from registration import Registration
from windowUser import MainWindowUser
from mariaDB_users import MariaDBUsers


class Authorization(QWidget):
    def __init__(self):
        super().__init__()
        self.mariaUser = MariaDBUsers()
        self.initializeUI()

    def initializeUI(self):
        """ Initialize thw window and display its contents to the screen (Authorization window) """
        self.setFixedSize(320, 260)
        self.setWindowTitle('Окно авторизации')
        self.displayLineEditor()
        self.displayButton()
        self.displayCheckBox()
        self.displayLine()

        self.show()

    def displayLineEditor(self):
        """ Display Line Editor with placeholder (Username, Password) """
        self.user_name = QLineEdit(self)
        self.user_name.setPlaceholderText(" Имя пользователя")
        self.user_name.move(50, 30)
        self.user_name.resize(235, 30)

        self.password = QLineEdit(self)
        self.password.setPlaceholderText(" Пароль")
        self.password.move(50, 70)
        self.password.resize(235, 30)

    def displayButton(self):
        """ Display Button (sign in, sign up, cancel) """
        sign_in = QPushButton('Войти', self)
        sign_in.move(15, 110)
        sign_in.resize(95, 25)
        sign_in.clicked.connect(self.event_sign_in)

        sign_up = QPushButton('Регистрация', self)
        sign_up.move(115, 110)
        sign_up.resize(95, 25)
        sign_up.clicked.connect(self.event_sign_up)

        cancel = QPushButton('Отмена', self)
        cancel.move(215, 110)
        cancel.resize(95, 25)
        cancel.clicked.connect(self.event_cancel)

    def displayCheckBox(self):
        """ Display CheckBox (Remember, Show password) """
        self.remember = QCheckBox('Запомнить меня', self)
        self.remember.move(70, 150)
        # self.remember.stateChanged.connect(self.event_remember)
        self.remember.toggle()
        self.remember.setChecked(False)

        show_password = QCheckBox('Показать пароль', self)
        show_password.move(70, 170)
        show_password.stateChanged.connect(self.event_show_password)
        show_password.toggle()
        show_password.setChecked(False)

    def displayLine(self):
        """ Display Line (Forgot password) """
        forgot_password = QLabel('<a href="#">Забыли пароль?</a>', self)
        forgot_password.move(80, 200)
        # font = QFont()
        # font.setPointSize(12)
        # font.setStyleStrategy(QFont.PreferAntialias)
        # forgot_password.setFont(font)
        forgot_password.linkActivated.connect(self.event_forgot_password)

    def event_sign_in(self):
        """ When user clicks sign in button, check if username and password match any existing profiles in users.txt
        If they exist, program goes to main menu.
        If they don't, display error messagebox. ("The username or password is incorrect.") """
        username = self.user_name.text()
        password = self.password.text()
        if username == '':
            # self.main_dialog = Main('oasis')
            self.main_dialog = MainWindowUser('phokeboy')
            # self.main_dialog = MainWindowUser('oasis')
            # self.main_dialog = MainWindowUser('terror')
            # self.main_dialog = MainWindowUser('phokeboy')
            self.main_dialog.show()
        if username:
            verification = self.mariaUser.verification(username, password)
            if verification:
                with open('cookie.txt', 'w') as cookie:
                    if self.remember.isChecked():
                        cookie.write(str(self.user_name.text()))
                    else:
                        cookie.write('')
                self.main_dialog = MainWindowUser(self.user_name.text())
                self.main_dialog.show()
                self.hide()
            else:
                QMessageBox.warning(self, "Error Message", "Пользователь с такими данными не найден.", QMessageBox.Close)
        else:
            QMessageBox.warning(self, "Error Message", "Пользователь с такими данными не найден.", QMessageBox.Close)

    def event_sign_up(self):
        """ When the sign up button is clicked, open a new window and allow the ser to create a new account """
        self.registration_dialog = Registration()
        self.registration_dialog.show()

    def event_cancel(self):
        """ When asking the user will close the window authorization"""
        self.close()

    def event_show_password(self, state):
        """ if checkbox is enabled, view password. Else, mask password so others cannot see it """
        if state == Qt.Checked:
            self.password.setEchoMode(QLineEdit.Normal)
        else:
            self.password.setEchoMode(QLineEdit.Password)

    def event_forgot_password(self):
        self.password_recovery_dialog = PasswordRecovery()
        self.password_recovery_dialog.show()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            self.event_sign_in()
