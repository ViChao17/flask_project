import sqlite3
import os
from flask import Flask, render_template, request, g
import config
from FDataBase import FDataBase


app = Flask(__name__)
app.config.from_object(config.__name__)
app.config.update(dict(DATABASE = os.path.join(app.root_path, 'flsite.db')))

def connectDB():
    connect = sqlite3.connect(app.config['DATABASE'])
    connect.row_factory = sqlite3.Row
    return connect

def getDB():
    if not hasattr(g, 'link_db'):
        g.link_db = connectDB()
    return g.link_db

@app.route("/")
def index():
    db = getDB()
    fdb = FDataBase(db)
    return render_template('index.html', menu = fdb.getMenu())

@app.teardown_appcontext
def closeDB(error):
    if hasattr(g, 'link_db'):
        g.link_db.close()

def createDB():
    db = connectDB()
    with app.open_resource('sq_db.sql', mode='r') as file:
        db.cursor().executescript(file.read())
    db.commit()
    db.close()
    
if __name__ == '__main__':
    app.run(debug=True)