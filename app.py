from flask import Flask, request, render_template, redirect
import psycopg2
from psycopg2 import sql

app = Flask(__name__)

# Функция для создания базы данных, если она не существует
def create_database():
    connection = psycopg2.connect(
        dbname='postgres',  # Подключаемся к базе данных по умолчанию
        user='postgres',
        password='vlad',
        host='db',
        port='5432'
    )
    connection.autocommit = True  # Включаем автоматическое подтверждение
    cursor = connection.cursor()

    # Создание базы данных, если она не существует
    cursor.execute(sql.SQL("SELECT 1 FROM pg_database WHERE datname = %s"), ['mydatabase'])
    exists = cursor.fetchone()
    if not exists:
        cursor.execute(sql.SQL("CREATE DATABASE {}").format(sql.Identifier('mydatabase')))
        print("База данных 'mydatabase' создана.")

    cursor.close()
    connection.close()

# Создание базы данных при запуске приложения
create_database()

# Настройка подключения к PostgreSQL
conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres",
    password="vlad",
    host="db",
    port="5432"
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

# Функция для создания таблицы, если она не существует
def create_table():
    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id SERIAL PRIMARY KEY,
        name VARCHAR(100),
        email VARCHAR(100)
    )
    """)
    conn.commit()

# Создание таблицы при запуске приложения
create_table()

@app.route('/')
def index():
    # Получение данных из таблицы
    cur.execute("SELECT * FROM users")
    users = cur.fetchall()
    return render_template('index.html', users=users)

@app.route('/add_user', methods=['POST'])
def add_user():
    # Получение данных из формы
    name = request.form['name']
    email = request.form['email']

    # Вставка данных в таблицу
    cur.execute("INSERT INTO users (name, email) VALUES (%s, %s)", (name, email))
    conn.commit()
    return redirect('/')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')  # Убедитесь, что приложение доступно извне контейнера
##