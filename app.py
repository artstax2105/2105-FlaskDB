import requests
from flask import Flask, render_template, request, redirect
import psycopg2
#создали приложение
app = Flask(__name__)
#подключились к бд
conn = psycopg2.connect(database="service_db",
                        user="postgres",
                        password="",
                        host="localhost",
                        port="5432")
#добавили курсор
cursor = conn.cursor()
# создаем декоратор
@app.route('/login/', methods=['POST', 'GET'])
def login():
    #исключение на проверку пост
    if request.method == 'POST':
        if request.form.get("login"):
            username = request.form.get('username')
            password = request.form.get('password')
            cursor.execute("SELECT * FROM service.users WHERE login=%s AND password=%s", (str(username), str(password)))
            records = list(cursor.fetchall())
#исключение на пустой ввод
            if username and password and records:
                #рендер страницы аккаунт
                return render_template('account.html', full_name=records[0][1], log=username, pas=password)
        elif request.form.get("registration"):
            #перенаправление на регистрацию
            return redirect("/registration/")
    # рендер страницы регистрация
    return render_template('login.html')

#декоратор2
@app.route('/registration/', methods=['POST', 'GET'])
def registration():
    #проверка на пост
    if request.method == 'POST':
        name = request.form.get('name')
        login = request.form.get('login')
        password = request.form.get('password')
        # проверка на исключения
        if str(name) and str(login) and str(password):
            #обращение к бд
            cursor.execute("SELECT * FROM service.users WHERE login=%s", (str(login),))
            records = cursor.fetchall()
            if records:
                return redirect("/registration/")
            else:
                cursor.execute('INSERT INTO service.users (full_name, login, password) VALUES (%s, %s, %s);', (str(name), str(login), str(password)))
                return redirect('/login/')
#внесение изменений в бд
        conn.commit()
# рендер регистрации
    return render_template('registration.html')