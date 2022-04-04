# Phone_book
new

Что умеет:
Добавлять контакты в "телефонную книжку",
Удалять, обновлять контакты,
Напоминать об именинниках на ближайшую неделю,

Доп возможности:
Запомнить при входе

Руководство:
Создать БД: CREATE DATABASE IF NOT EXISTS users;
user = 'Имя_пользователя'
password = 'Пароль'
port = 3306 (можно любой удобный)
и заполнить данные в mariaDB_users.py и mariaDB_contacts.py. 
Т.к. server mariadb - имеет host = localhost

Схема БД, описана в файлах mariaDB_users.py и mariaDB_contacts.py

Для открытия приложения нужно запустить файл application.py
