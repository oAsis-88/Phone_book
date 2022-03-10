# mariaDB_users.py
import mariadb
import sys

"""
CREATE TABLE IF NOT EXISTS users(
           id INT NOT NULL AUTO_INCREMENT,
           user VARCHAR(30) NOT NULL UNIQUE,
           password VARCHAR(30) NOT NULL,
           birth DATE NOT NULL,
           PRIMARY KEY (id));
"""


class MariaDBUsers():
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
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"not connecting to MariaDB users Platform")
            sys.exit(1)

    def add(self, user_, password_, birth_):
        try:
            sql = "INSERT IGNORE INTO users (user, password, birth) VALUES (?, ?, ?)"
            data = [(user_, password_, birth_)]
            self.cursor.executemany(sql, data)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB users: '{user_}', '{password_}' not added")
            sys.exit(1)

    def update(self, user, password):
        try:
            sql = "UPDATE users SET password=? WHERE user=?"
            data = [(password, user)]
            self.cursor.executemany(sql, data)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB users: '{user}', '{password}' not updated")
            sys.exit(1)

    def remove(self, *user):
        try:
            sql = "DELETE FROM users WHERE user=?"
            data = [(x,) for x in user]
            # print('data -', data)
            self.cursor.executemany(sql, data)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB users: '{user}' not removed")
            sys.exit(1)

    def removeAll(self):
        try:
            sql = "DELETE FROM users"
            self.cursor.execute(sql)
            self.connection.commit()
        except mariadb.Error as e:
            print(f"Error: {e}")
            print("MariaDB users: not removed all")
            sys.exit(1)

    def get(self, user):
        try:
            sql = f"SELECT user, password FROM users WHERE user='{user}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            return result
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB users: '{user}' not found (get)")
            sys.exit(1)

    def verification(self, user_, password_):
        try:
            sql = f"SELECT password FROM users WHERE user='{user_}'"
            self.cursor.execute(sql)
            result = self.cursor.fetchall()
            if result:
                return result[0][0] == password_
            return False
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB users: '{user_}' not found (get)")
            sys.exit(1)

    def printAllTable(self):
        try:
            self.cursor.execute("SELECT * FROM users;")
            result = self.cursor.fetchall()
            print('--------------------')
            for r in result:
                print(r)
            print('--------------------')
        except mariadb.Error as e:
            print(f"Error: {e}")
            print(f"MariaDB users: not printed")
            sys.exit(1)

    def show(self):
        self.cursor.execute("SHOW DATABASES")
        print(self.cursor.fetchall())
        self.cursor.execute("SHOW TABLES")
        print(self.cursor.fetchall())
        self.cursor.execute("SHOW TABLES")
        print(self.cursor.fetchall())
