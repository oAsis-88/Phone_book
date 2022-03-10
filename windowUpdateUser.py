# windowUpdateUser.py
from datetime import datetime

from PyQt5.QtCore import Qt, QDate
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QLineEdit, QDateEdit, QHBoxLayout, QPushButton, QMessageBox


class UpdateUser(QWidget):
    def __init__(self, user_, name_, phone_, birth_, database, table_contact):
        super().__init__()
        self.user_ = user_
        self.old_name_ = name_
        self.old_phone_ = phone_
        self.old_birth_ = datetime.strptime(birth_, '%d-%m-%Y').strftime('%Y-%m-%d')
        self.mariaContacts = database
        self.table_contact = table_contact
        self.initializeUI()

        with open("style.txt", 'r') as f:
            style = f.read()
            self.setStyleSheet(style)

    def initializeUI(self):
        self.setFixedSize(170, 150)
        vbox = QVBoxLayout()
        self.new_name = QLineEdit(self.old_name_)
        self.new_phone = QLineEdit(self.old_phone_)
        self.new_birth = QDateEdit()
        self.new_birth.setDisplayFormat('yyyy-MM-dd')
        self.new_birth.setDate(QDate.fromString(self.old_birth_, "yyyy-MM-dd"))
        # Установите контроль календаря, чтобы разрешить всплывающее окно
        self.new_birth.setCalendarPopup(True)
        # Установите максимальные и минимальные даты, основываясь на текущей дате, следующем году и предыдущем году
        # self.dateEdit.setMinimumDate(QDate.currentDate().addDays(-365))
        self.new_birth.setMaximumDate(QDate.currentDate().addDays(0))

        hbox = QHBoxLayout()
        ok = QPushButton("Ok")
        ok.setObjectName("BtnGreen")
        ok.clicked.connect(self.event_ok)
        cancel = QPushButton("Close")
        cancel.setObjectName("BtnRed")
        cancel.clicked.connect(self.event_close)
        hbox.addWidget(ok)
        hbox.addWidget(cancel)
        vbox.addWidget(self.new_name)
        vbox.addWidget(self.new_phone)
        vbox.addWidget(self.new_birth)
        vbox.addLayout(hbox)
        self.setLayout(vbox)
        self.show()

    def event_ok(self):
        if not self.new_name.text() or not self.new_phone.text() or not self.new_birth.text():
            QMessageBox.warning(self, "Error Message", "Заполните все поля.", QMessageBox.Close)
        else:
            update_boolean = self.mariaContacts.update(self.user_,
                                                       self.old_name_, self.new_name.text(),
                                                       self.old_phone_, self.new_phone.text(),
                                                       self.old_birth_, self.new_birth.text())
            if update_boolean:
                self.table_contact.clearContents()
                self.table_contact.setupUI()
                self.close()
            else:
                qm = QMessageBox.warning(self, "Error Message", "Такой пользователь уже существует.\n Удалить?",
                                         QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
                if qm == QMessageBox.Yes:
                    self.mariaContacts.remove(self.user_, self.old_name_, self.old_phone_, self.old_birth_)
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
