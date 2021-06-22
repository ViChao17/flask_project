import sqlite3
from flask import abort, redirect, flash, render_template
from flask import Flask, request, session, g
from flask.helpers import url_for
import config
import os
from FDataBase import FDataBase

app = Flask(__name__)
app.config.from_object(config.__name__)
app.config.update(dict(DATABASE = os.path.join(app.root_path, 'flsite.db')))

@app.route("/")
def index():
    return render_template('index.html', menu = FDataBase(getDB()).getMenu(), session = session)

@app.route("/about/")
def about():
    return render_template('about.html', title = "О сайте", menu = FDataBase(getDB()).getMenu(), session = session)

@app.route("/profile/<username>", methods=["POST", "GET"])
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)

    fdb = FDataBase(getDB())
    if request.method == 'POST':
        print('okokokokokokokoo')
        fdb.updateUserInfoById(session['userId'], request.form['name'], request.form['info'])
    print(session['userId'])
    return render_template("profile.html", title = "Профиль", menu = fdb.getMenu(), user = fdb.getUserById(session['userId']), session = session)

@app.route("/authorization/", methods=["POST", "GET"])
def authorization():
    if request.method == 'POST':
        print(request.form)
    if 'userLogged' in session:
        return redirect(url_for('profile', username = session['userLogged']))
    elif request.method == 'POST':
        fdb = FDataBase(getDB())
        user = dict(fdb.getUserIdByLoginPass(request.form['login'], request.form['pass']))
        if 'id' in user:
            session['userLogged'] = request.form['login']
            session['userId'] = user['id']
            return redirect(url_for('profile', username = session['userLogged']))
    
    return render_template('authorization.html', title = "Авторизация", menu = FDataBase(getDB()).getMenu(), session = session)

@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        print(request.form)
    return render_template('register.html', title = "Регистрация", menu = FDataBase(getDB()).getMenu(), session = session)

@app.route("/contact/", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash("Сообщение отправлено!")
        else:
            flash("Ошибка отправки")
        print(request.form)
    return render_template('contact.html', title = "Обратная связь", menu = FDataBase(getDB()).getMenu(), session = session)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('errorpage.html', title = "Страница не найдена", menu = FDataBase(getDB()).getMenu(), session = session), 404

@app.teardown_appcontext
def closeDB(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def connectDB():
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect

def getDB():
    if not hasattr(g, 'link_db'):
        g.link_db = connectDB()
    return g.link_db

def createDB():
    db = connectDB()
    with app.open_resource('sq_db.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()

if __name__== "__main__":
    app.run(debug=False)