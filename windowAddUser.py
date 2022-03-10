# windowAddUser.py
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QDateEdit, QHBoxLayout, QPushButton, QMessageBox, QDialog


class AddUser(QDialog):
    def __init__(self, user, database, table_contact):
        super().__init__()
        self.user = user
        self.mariaContacts = database
        self.table_contact = table_contact
        self.initializeUI()

        with open("style.txt", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

    def initializeUI(self):
        self.setFixedSize(170, 150)
        vBox = QVBoxLayout(self)
        self.name = QLineEdit()
        self.name.setPlaceholderText('name')
        self.phone = QLineEdit()
        self.phone.setPlaceholderText('phone')
        self.birth = QDateEdit()
        self.birth.setDisplayFormat('yyyy-MM-dd')
        hBox = QHBoxLayout()
        ok = QPushButton("Ok")
        ok.setObjectName("BtnGreen")
        ok.clicked.connect(self.event_ok)
        cancel = QPushButton("Close")
        cancel.setObjectName("BtnRed")
        cancel.clicked.connect(self.event_close)
        hBox.addWidget(ok)
        hBox.addWidget(cancel)
        vBox.addWidget(self.name)
        vBox.addWidget(self.phone)
        vBox.addWidget(self.birth)
        vBox.addLayout(hBox)
        self.setLayout(vBox)
        self.show()

    def event_ok(self):
        if not self.name.text() or not self.phone.text() or not self.birth.text():
            QMessageBox.warning(self, "Error Message", "Заполните все поля.", QMessageBox.Close)
        else:
            self.mariaContacts.add(self.user, self.name.text(), self.phone.text(), self.birth.text())
            self.table_contact.clearContents()
            self.table_contact.setupUI()
            self.close()

    def event_close(self):
        self.close()

    def keyPressEvent(self, e):
        if e.key() == Qt.Key_Escape:
            self.close()
        elif e.key() == Qt.Key_Return:
            self.event_ok()
