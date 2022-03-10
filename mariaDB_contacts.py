# mariaDB_contacts.py
import mariadb
import sys

"""
CREATE TABLE IF NOT EXISTS contacts(
           user VARCHAR(30) NOT NULL,
           name VARCHAR(30) NOT NULL,
           phone VARCHAR(30) NOT NULL,
           birth DATE NOT NULL);
"""


class MariaDBContacts():
    def __init__(self):
        try:
            self.connection = mariadb.connect(
                user="root",
                password="root",
                host="localhost",
                port=3306,
                database="users",
                autocommit=True
            )
            self.cursor = self.connection.cursor()
            sql = "SET lc_time_names = 'ru_RU';"
            self.cursor.execute(sql)
            # print("---- connecting to MariaDB contacts ----")
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"not connecting to MariaDB contacts Platform")
            sys.exit(1)

    def add(self, user_, name_, phone_, birth_):
        try:
            sql = f"SELECT user, name, phone, birth FROM contacts WHERE user='{user_}' AND name='{name_}' AND phone='{phone_}' AND birth='{birth_}'"
            self.cursor.execute(sql)
            if not self.cursor.fetchall():
                sql = "INSERT IGNORE INTO contacts (user, name, phone, birth) VALUES (?, ?, ?, ?)"
                data = [(user_, name_, phone_, birth_)]
                self.cursor.executemany(sql, data)
                self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}', '{name_}', '{phone_}', '{birth_}' not added")
            sys.exit(1)

    def update(self, user_, old_name_, new_name_, old_phone_, new_phone_, old_birth_, new_birth_):
        try:
            sql = f"SELECT user, name, phone, birth FROM contacts " \
                  f" WHERE user='{user_}' AND name='{new_name_}' AND phone='{new_phone_}' AND birth='{new_birth_}'"
            self.cursor.execute(sql)
            if not self.cursor.fetchall():
                sql = f"UPDATE contacts SET name='{new_name_}', phone='{new_phone_}', birth='{new_birth_}' " \
                      f" WHERE user='{user_}' AND name='{old_name_}' AND phone='{old_phone_}' AND birth='{old_birth_}'"

                self.cursor.execute(sql)
                self.connection.commit()
                return True
            return False

        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: not updated")
            # print(f"MariaDB contacts: '{user_}', '{name_}', '{phone_}', '{birth_}' not updated")
            sys.exit(1)

    def remove(self, user_, name_, phone_, birth_):
        try:
            sql = f"DELETE FROM contacts WHERE user='{user_}' AND name='{name_}' AND phone='{phone_}' AND birth='{birth_}'"
            self.cursor.execute(sql)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}', '{name_}' not removed")
            sys.exit(1)

    def removeAll(self, user_):
        try:
            sql = f"DELETE FROM contacts WHERE user='{user_}'"
            self.cursor.execute(sql)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}' not removed all")
            sys.exit(1)

    def clear(self):
        try:
            sql = f"DELETE FROM contacts "
            self.cursor.execute(sql)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: not cleared")
            sys.exit(1)

    def get(self, user_, name_):
        try:
            sql = f"SELECT name, phone, birth FROM contacts WHERE user='{user_}' AND name='{name_}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}' not found (get)")
            sys.exit(1)

    def get_contacts_with_birth(self, user_):
        try:
            sql = f"SELECT name, phone, DATE_FORMAT(birth,'%d %M %Y') FROM contacts " \
                  f"WHERE user='{user_}' AND (DAYOFYEAR(birth) - DAYOFYEAR(NOW())) <= 7 AND (DAYOFYEAR(birth) - DAYOFYEAR(NOW())) > 0;"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}' not found (get)")
            sys.exit(1)

    def get_all_contacts(self, user_):
        try:
            sql = f"SELECT name, phone, birth FROM contacts WHERE user='{user_}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}' not found (get)")
            sys.exit(1)

    def get_name_by_symbol(self, user_, char_):
        try:
            result = []
            for i in list(char_):
                sql = f"SELECT name, phone, birth FROM contacts WHERE user='{user_}' AND name LIKE '{i}%'"
                self.cursor.execute(sql)
                names = self.cursor.fetchall()
                for el in names:
                    element = (el[0], el[1], el[2].strftime('%d-%m-%Y'))
                    result.append(element)
            return result
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: '{user_}' not found (get)")
            sys.exit(1)

    def count_users(self, user_, char_):
        result = 0
        for i in list(char_):
            sql = f"SELECT COUNT(*) as count FROM contacts WHERE user='{user_}' AND name LIKE '{i}%'"
            self.cursor.execute(sql)
            result += self.cursor.fetchall()[0][0]
        return result

    def printAllTableUser(self, user_):
        try:
            sql = f"SELECT name, phone, birth FROM contacts WHERE user='{user_}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            print('--------------------')
            for r in result:
                print(f"{r[0]}, {r[1]}, {r[2].strftime('%d %B, %Y')}")
            print('--------------------')
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: not printed")
            sys.exit(1)

    def printAllTable(self):
        try:
            self.cursor.execute("SELECT * FROM contacts;")
            result = self.cursor.fetchall()
            print('--------------------')
            for r in result:
                print(f"{r[0]}, {r[1]}, {r[2]}, {r[3].strftime('%d %B, %Y')}")
            print('--------------------')
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB contacts: not printed")
            sys.exit(1)

    def show(self):
        self.cursor.execute("SHOW DATABASES")
        print(self.cursor.fetchall())
        self.cursor.execute("SHOW TABLES")
        print(self.cursor.fetchall())
