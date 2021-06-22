from flask import abort
from flask import Flask, render_template, request, flash, session, redirect
from flask.helpers import url_for

app = Flask(__name__)

app.config['SECRET_KEY'] = 'dshf8f7230fhje9492jdklsdl'

menu = [{"title": "О сайте", "url": "/about"},
        {"title": "Авторизация", "url": "/authorization"},
        {"title": "Регистрация", "url": "/register"},
        {"title": "Обратная связь", "url": "/contact"}]

@app.route("/home/")
@app.route("/index/")
@app.route("/")
def index():
    return render_template('index.html', menu = menu)

@app.route("/about/")
def about():
    return render_template('about.html', title = "О сайте", menu = menu)

@app.route("/profile/<username>")
def profile(username):
    if 'userLogged' not in session or session['userLogged'] != username:
        abort(401)
    return render_template("profile.html", title = "Профиль", menu = menu, session = session)

@app.route("/authorization/", methods=["POST", "GET"])
def authorization():
    if request.method == 'POST':
        print(request.form)
    if 'userLogged' in session:
        #print(session['userLogged'])
        return redirect(url_for('profile', username = session['userLogged']))
    elif request.method == 'POST' and request.form['login'] == "victor" and request.form['pass'] == "qwerty":
        session['userLogged'] = request.form['login']
        #print(session['userLogged'])
        return redirect(url_for('profile', username = session['userLogged']))
    
    return render_template('authorization.html', title = "Авторизация", menu = menu)

@app.route("/register/", methods=["POST", "GET"])
def register():
    if request.method == 'POST':
        print(request.form)
    return render_template('register.html', title = "Регистрация", menu = menu)

@app.route("/contact/", methods=["POST", "GET"])
def contact():
    if request.method == 'POST':
        if len(request.form['name']) > 2:
            flash("Сообщение отправлено!")
        else:
            flash("Ошибка отправки")
        print(request.form)
    return render_template('contact.html', title = "Обратная связь", menu = menu)

@app.errorhandler(404)
def pageNotFound(error):
    return render_template('errorpage.html', title = "Страница не найдена", menu = menu), 404

if __name__== "__main__":
    app.run()