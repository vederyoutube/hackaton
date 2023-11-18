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
email_var = StringVar()
email_var.set("Электронная почта")
email_entry = Entry(root, textvariable=email_var)
email_entry.pack()

password_var = StringVar()
password_var.set("Пароль")
password_entry = Entry(root, show="*", textvariable=password_var)
password_entry.pack()

# Функции для очистки и восстановления текста
def clear_placeholder(event, entry, placeholder):
    if entry.get() == placeholder:
        entry.delete(0, END)

def restore_placeholder(event, entry, placeholder):
    if not entry.get():
        entry.insert(0, placeholder)

# Привязываем функции к событиям фокуса
email_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, email_entry, "Электронная почта"))
email_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, email_entry, "Электронная почта"))

password_entry.bind("<FocusIn>", lambda event: clear_placeholder(event, password_entry, "Пароль"))
password_entry.bind("<FocusOut>", lambda event: restore_placeholder(event, password_entry, "Пароль"))

# Кнопка для входа
login_button = Button(root, text="Войти", command=login)
login_button.pack()

# Запускаем главный цикл
root.mainloop()