import mysql.connector
from tkinter import *
import hashlib

def login():
    # Получаем данные из полей формы
    email = email_entry.get()
    password = password_entry.get()

    # Подключение к базе данных
    connection = mysql.connector.connect(
        host="141.8.192.151",
        user="f0878880_VaniVl",
        password="228338ljv",
        database="f0878880_massager"
    )

    # Создаем объект cursor для выполнения SQL-запросов
    cursor = connection.cursor()

    try:
        # SQL-запрос для получения пользователя по электронной почте и паролю
        sql = "SELECT * FROM users WHERE email = %s AND password = %s"
        hashed_password = hashlib.sha256(password.encode()).hexdigest()
        data = (email, hashed_password)

        # Выполняем запрос
        cursor.execute(sql, data)
        user = cursor.fetchone()

        if user:
            login_button.config(text="Вход успешен")
        else:
            login_button.config(text="Неверные электронная почта или пароль")

    except Exception as e:
        login_button.config(text="Ошибка входа")

    finally:
        # Закрываем соединение
        connection.close()

# Создаем графический интерфейс
root = Tk()
root.title("Вход в учетную запись")

# Создаем метки и поля для ввода данных
email_label = Label(root, text="Электронная почта:")
email_label.pack()
email_entry = Entry(root)
email_entry.pack()

password_label = Label(root, text="Пароль:")
password_label.pack()
password_entry = Entry(root, show="*")
password_entry.pack()

# Кнопка для входа
login_button = Button(root, text="Войти", command=login)
login_button.pack()

# Запускаем главный цикл
root.mainloop()