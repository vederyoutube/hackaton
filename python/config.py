import mysql.connector
from tkinter import *

def save_to_database():
    # Получаем данные из полей формы
    username = username_entry.get()
    password = password_entry.get()

    # Проверка длины пароля
    if len(password) < 6:
        save_button.config(text="Пароль должен быть больше 6 символов")
        return

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
        # SQL-запрос для вставки данных
        sql = "INSERT INTO users (username, password) VALUES (%s, %s)"
        data = (username, password)

        # Выполняем запрос
        cursor.execute(sql, data)

        # Подтверждаем изменения
        connection.commit()

        # Восстанавливаем текст кнопки после успешной операции
        save_button.config(text="Регистрация успешна")

        # Очищаем поля формы после сохранения
        username_entry.delete(0, END)
        password_entry.delete(0, END)

    except mysql.connector.IntegrityError as e:
        if "Duplicate entry" in str(e):
            save_button.config(text="Имя пользователя занято")
        else:
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

# Кнопка для сохранения данных
save_button = Button(root, text="Зарегистрироваться", command=save_to_database)
save_button.pack()

# Запускаем главный цикл
root.mainloop()