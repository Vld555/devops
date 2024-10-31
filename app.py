from flask import Flask, request, render_template, redirect
import psycopg2

app = Flask(__name__)

# Настройка подключения к PostgreSQL
conn = psycopg2.connect(
    dbname="mydatabase",
    user="postgres",
    password="vlad",
    host="localhost",
    port="5432"
)

# Создание курсора для выполнения SQL-запросов
cur = conn.cursor()

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
    app.run(debug=True)
