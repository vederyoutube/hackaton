import mysql.connector
from tkinter import *
import hashlib
import re

def check_username_in_database(username):
    # Подключение к базе данных
    connection = mysql.connector.connect(
        host="141.8.192.151",
        user="f0878880_VaniVl",
        password="228338ljv",
        database="f0878880_massager"
    )

    # Создаем объект cursor для выполнения SQL-запросов
    cursor = connection.cursor()

    # SQL-запрос для проверки наличия пользователя с таким именем
    cursor.execute("SELECT * FROM users WHERE username = %s", (username,))
    existing_user = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    return existing_user is not None

def check_mail_in_database(email):
    # Подключение к базе данных
    connection = mysql.connector.connect(
        host="141.8.192.151",
        user="f0878880_VaniVl",
        password="228338ljv",
        database="f0878880_massager"
    )

    # Создаем объект cursor для выполнения SQL-запросов
    cursor = connection.cursor()

    # SQL-запрос для проверки наличия пользователя с таким именем
    cursor.execute("SELECT * FROM users WHERE email = %s", (email,))
    existing_user = cursor.fetchone()

    # Закрываем соединение
    connection.close()

    return existing_user is not None

def save_to_database():
    # Получаем данные из полей формы
    username = username_entry.get()
    password = password_entry.get()
    email = email_entry.get()

    # Проверка длины пароля
    if len(password) < 6:
        save_button.config(text="Пароль должен быть больше 6 символов")
        return
    
     # Шифруем пароль
    hashed_password = hashlib.sha256(password.encode()).hexdigest()

    # Проверка наличия пользователя с таким именем
    if check_username_in_database(username):
        save_button.config(text="Имя пользователя занято")
        return
    
    # Проверка наличия пользователя с такой же почтой
    if check_mail_in_database(email):
        save_button.config(text="Уже есть учетная запись с такой почтой")
        return
    
    # Проверка корректности введенной электронной почты
    email_pattern = re.compile(r"[^@]+@[^@]+\.[^@]+")
    if not re.match(email_pattern, email):
        save_button.config(text="Некорректный адрес электронной почты")
        return

    # Подключеие к базе данных
    connection = mysql.connector.connect(
        host="141.8.192.151",
        user="f0878880_VaniVl",
        password="228338ljv",
        database="f0878880_massager"
    )

    # Создаем объект cursor для выполнения SQL-запросов
    cursor = connection.cursor()

    try:
        # SQL-запрос для вставки данных
        sql = "INSERT INTO users (username, password, email) VALUES (%s, %s, %s)"
        data = (username, hashed_password, email)

        # Выполняем запрос
        cursor.execute(sql, data)

        # Подтверждаем изменения
        connection.commit()

        # Восстанавливаем текст кнопки после успешной операции
        save_button.config(text="Регистрация успешна")

        # Очищаем поля формы после сохранения
        username_entry.delete(0, END)
        password_entry.delete(0, END)
        email_entry.delete(0, END)

    except mysql.connector.IntegrityError as e:
        save_button.config(text="Ошибка регистрации")

    finally:
        # Закрываем соединение
        connection.close()

# Создаем графический интерфейс
root = Tk()
root.title("Регистрация")

# Создаем метки и поля для ввода данных
username_label = Label(root, text="Имя пользователя:")
username_label.pack()
username_entry = Entry(root)
username_entry.pack()

password_label = Label(root, text="Пароль:")
password_label.pack()
password_entry = Entry(root, show="*")
password_entry.pack()

email_label = Label(root, text="Электронная почта:")
email_label.pack()
email_entry = Entry(root)
email_entry.pack()

# Кнопка для сохранения данных
save_button = Button(root, text="Зарегистрироваться", command=save_to_database)
save_button.pack()

# Запускаем главный цикл
root.mainloop()