from flask import Flask, request, make_response, redirect, url_for, render_template

app = Flask(__name__)

import sqlite3
from flask import g

DATABASE = 'database.db'


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()

def create_session(): pass

@app.route('/')
def main_page():
    # if user has valid cookie, redirect to main page
    # else redirect to login
    return


@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        # resp = make_response(redirect(url_for('/')))
        # resp.set_cookie('s_id', )
    else:
        resp = make_response(render_template('login.html'))
    pass


@app.route('/create', methods=['post'])
def create_user():
    email = request.form['email']
    password = request.form['password']

    conn = get_db()
    # todo check if user exists
    cursor = conn.cursor()
    cursor.execute('INSERT INTO users (email, password) values (?,?)')




@app.route('/club/<club_id>')
def get_club(club_id):
    pass


if __name__ == '__main__':
    app.run(port=8080)
