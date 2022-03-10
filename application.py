from datetime  import datetime
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

    # from mariaDB_contacts import MariaDBContacts
    # maria = MariaDBContacts()
    # maria.count_users('terror', 'ВГ')
    # maria.get_name_by_symbol('terror', 'ВГ')
    # print("ALL TABLE")
    # maria.printAllTable()
    # print("\nADD")
    # maria.add('oasis', 'Горина Анастасия', '+7345675334', '1995-08-05')
    # maria.add('oasis', 'Васин Василий', '+7213345324', '2000-06-04')
    # maria.add('oasis', 'Андрей Георг', '+752617323', '1999-08-31')
    # maria.add('oasis', 'Васин Василий', '+78919412', '1990-12-24')
    # maria.add('terror', 'Максим Цапен', '+747132929', '1995-08-05')
    # maria.add('terror', 'Гаврилина Мария', '+7678964567', '2015-01-21')
    # maria.add('terror', 'Александрович Александр', '+732732546', '2002-09-30')
    # maria.add('terror', 'Андрей Вац', '+771292354', '2000-02-03')
    # maria.add('terror', 'Арнольд Порт', '+788911891', '2006-07-28')
    # print("\nALL TABLE oasis")
    # maria.printAllTableUser('oasis')
    # print("\nUPDATE")
    # maria.update('oasis', 'Горина Анастасия', '+78', '2000-06-04')
    # maria.printAllTable()
    # print("\nREMOVE")
    # maria.remove('oasis', 'Горина Анастасия')
    # maria.remove('oasis', 'Васин Василийa')
    # print("\nREMOVEALL")
    # maria.removeAll('oasis')
    # maria.removeAll('phokeboy')
    # maria.removeAll('terror')
    # print("\nCLEAR CONTACTS")
    # maria.clear()
    # print("\nGET")
    # maria.get('oasis', 'Горина Анастасия')
    # print("\nGET")
    # maria.get('oasis', 'admin')



    # from mariaDB_users import MariaDBUsers
    # maria = MariaDBUsers()
    # # print("\nSHOW")
    # # maria.show()
    # # print("\nALL TABLE")
    # # maria.printAllTable()
    # print("\nADD")
    # maria.add('oasis', '1234', '2002.03.11')
    # maria.add('terror', 'qwe', '2011.11.11')
    # maria.add('phokeboy', 'swd', '2002.09.06')
    # maria.printAllTable()
    # print("\nUPDATE")
    # maria.update('oasis', 'qwr')
    # maria.printAllTable()
    # print("\nREMOVE")
    # maria.remove('oasis')
    # maria.remove('o', 'a', 's', 'i', 's')
    # print("\nREMOVEALL")
    # maria.removeAll()
    # print("\nGET")
    # maria.get('oasis')
    # print("\nGET")
    # maria.get('oasis', 'admin')
