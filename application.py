from datetime import datetime
import sys
from PyQt5 import QtWidgets
from authorization import Authorization
from windowUser import MainWindowUser
from mariaDB_users import MariaDBUsers


def application():
    app = QtWidgets.QApplication(sys.argv)

    with open('cookie.txt', 'r') as cookie:
        data = cookie.readline()
        if data:
            user = data.strip().split()[0]
            if MariaDBUsers().get(user):
                m = MainWindowUser(user)
            else:
                m = Authorization()
        else:
            m = Authorization()

    m.show()
    sys.exit(app.exec_())


if __name__ == "__main__":
    application()
