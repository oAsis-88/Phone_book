from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton


class PasswordRecovery(QWidget):
    def __init__(self):
        super().__init__()
        self.initializeUI()

    def initializeUI(self):
        """ Initialize thw window and display its contents to the screen (Password recovery) """
        self.setFixedSize(320, 260)
        self.setWindowTitle('Восстановление пароля')
        self.displayLineEdit()
        self.displayButton()

        self.show()

    def displayLineEdit(self):
        """ Display Line Edit (email address) """
        email_address = QLineEdit(self)
        email_address.setPlaceholderText(' Адрес электронной почты')
        email_address.resize(220, 30)
        email_address.move(50, 75)

    def displayButton(self):
        """ Display Button (change password, cancel) """
        btn_change_password = QPushButton("Сменить пароль", self)
        btn_change_password.resize(100, 25)
        btn_change_password.move(50, 135)
        btn_change_password.clicked.connect(self.event_btn_change_password)

        btn_cancel = QPushButton("Отмена", self)
        btn_cancel.resize(110, 25)
        btn_cancel.move(160, 135)
        btn_cancel.clicked.connect(self.event_btn_cancel)

    def event_btn_change_password(self):
        """ Event Will send an email with password recovery. """
        pass

    def event_btn_cancel(self):
        """ Event close window password recovery"""
        self.close()
