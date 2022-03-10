# notification.py
import sys

# from PyQt5.QtWidgets import QWidget, QLineEdit, QPushButton, QApplication, QLabel
from PyQt5.QtCore import Qt
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *

from mariaDB_contacts import MariaDBContacts


class Notification(QDialog):
    def __init__(self, user_, contacts_, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.user_ = user_
        self.contacts_ = contacts_
        self.maria_contacts = MariaDBContacts()
        self.initializeUI()

        with open("style.txt", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

    def initializeUI(self):
        """ Initialize thw window and display its contents to the screen (Password recovery) """
        self.setMinimumWidth(360)
        self.adjustSize()
        self.setWindowTitle('Уведомление')
        self.setWindowFlags(Qt.WindowSystemMenuHint | Qt.WindowCloseButtonHint | Qt.WindowStaysOnTopHint)
        self.setWindowModality(Qt.ApplicationModal)

        self.font_word = QFont()
        self.font_word.setFamily("Arial")
        self.font_word.setPointSize(12)

        self.vbox = QVBoxLayout(self)
        self.displayHeading()
        self.displayContacts()
        self.show()

    def displayHeading(self):
        """ Display Line Edit (email address) """
        heading = QLabel()
        heading.setAlignment(Qt.AlignCenter)
        heading.setObjectName("Head")
        heading.setText(f"{self.user_}, у ваших контактов скоро др")

        fond_heading = self.font_word
        fond_heading.setBold(True)
        heading.setFont(fond_heading)

        self.vbox.addWidget(heading)

    def displayContacts(self):
        for i, el in enumerate(self.contacts_):
            widget = QWidget()
            widget.setObjectName("Contacts")
            label = QHBoxLayout()

            label_name = QLabel()
            label_name.setAlignment(Qt.AlignCenter)
            label_name.setObjectName("Name")
            label_name.setText(el[0])

            label_phone = QLabel()
            label_phone.setAlignment(Qt.AlignCenter)
            label_phone.setObjectName("Phone")
            label_phone.setText(el[1])

            label_birth = QLabel()
            label_birth.setAlignment(Qt.AlignCenter)
            label_birth.setObjectName("Birth")
            label_birth.setText(el[2])

            label.addWidget(label_name)
            label.addWidget(label_phone)
            label.addWidget(label_birth)
            widget.setLayout(label)
            self.vbox.addWidget(widget)

    def event_btn_cancel(self):
        """ Event close window password recovery"""
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    app.setStyleSheet(style_sheet)
    m = Notification(str('oasis'))
    m.show()
    sys.exit(app.exec_())
