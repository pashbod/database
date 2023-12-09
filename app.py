from flask import Flask, render_template, request, redirect, url_for
import sqlite3
from datetime import datetime

app = Flask(__name__)

# Конфігурації бази даних
DATABASE = 'managers.db'

# Функція для отримання підключення до бази даних
def get_db():
    db = sqlite3.connect(DATABASE)
    db.row_factory = sqlite3.Row
    return db

# Створення таблиці користувачів
def create_table():
    with get_db() as db:
        db.execute('''
            CREATE TABLE IF NOT EXISTS users (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                email TEXT NOT NULL,
                password TEXT NOT NULL,
                age INTEGER,
                gender TEXT,
                login_date TEXT
            )
        ''')
        db.commit()

# Реєстрація користувача
def register_user(email, password, age=None, gender=None):
    with get_db() as db:
        now = datetime.now()
        login_date = now.strftime("%Y-%m-%d %H:%M:%S")
        db.execute('''
            INSERT INTO users (email, password, age, gender, login_date)
            VALUES (?, ?, ?, ?, ?)
        ''', (email, password, age, gender, login_date))
        db.commit()

# Головна сторінка
@app.route('/')
def index():
    return render_template('index.html')

# Обробник для реєстрації
@app.route('/register', methods=['POST'])
def register():
    # Отримання даних з форми
    email = request.form['email']
    password = request.form['password']
    age = request.form.get('age', None)
    gender = request.form.get('gender', None)

    # Виклик функції для реєстрації користувача
    register_user(email, password, age, gender)

    # Перенаправлення на головну сторінку після реєстрації
    return redirect(url_for('index'))

# Запуск програми
if __name__ == '__main__':
    # Створення таблиці перед запуском
    create_table()
    # Запуск додатка Flask у режимі відладки
    app.run(debug=True)
