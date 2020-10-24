from flask import Flask, request, make_response, redirect, url_for, render_template, flash
import sqlite3
from flask import g

if False:
    from flask import Response

app = Flask(__name__)

DATABASE = 'database.db'


def dict_factory(cursor, row) -> dict:
    d = {}
    for idx, col in enumerate(cursor.description):
        d[col[0]] = row[idx]
    return d


def get_db():
    db = getattr(g, '_database', None)
    if db is None:
        db = g._database = sqlite3.connect(DATABASE)
        db.row_factory = dict_factory
    return db


@app.teardown_appcontext
def close_connection(exception):
    db = getattr(g, '_database', None)
    if db is not None:
        db.close()


def open_session(u_id):
    """
    :param u_id: user id
    :return: session id
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT session_id FROM sessions where user_id=?', (u_id,))
    value = cursor.fetchone()
    if not value:
        cursor.execute('INSERT INTO sessions (user_id, open) VALUES (?, true)', (u_id,))
    else:
        cursor.execute('UPDATE sessions SET open=true WHERE user_id=?', (u_id,))
    return cursor.execute('SELECT session_id FROM sessions where user_id=?', (u_id,)).fetchone()


def get_session(u_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT session_id FROM sessions WHERE user_id=?', (u_id,))
    return cursor.fetchone()


def get_user(session_id):
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT session_id FROM sessions WHERE session_id=?', (session_id,))
    return cursor.fetchone()


def close_session(u_id):
    """
    :param u_id: user id
    :return: nothing
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('UPDATE sessions SET open=false WHERE user_id=?', (u_id,))


def get_user_id(username, password):
    """
    :param username: username of account
    :param password: password of account
    :return: list of
    """
    conn = get_db()
    cursor = conn.cursor()
    cursor.execute('SELECT user_id FROM users where email=? and password=?', (username, password))
    res = cursor.fetchone()
    if res is not None:
        return res['user_id']


@app.route('/')
def main_page():
    # if user has valid cookie, redirect to main page
    # else redirect to login
    session_id = request.cookies.get('s_id')
    if not session_id:
        resp = redirect(url_for('login'))
        return resp

    u_id = get_user(session_id)

    return render_template('login.html')


@app.route('/login', methods=['post', 'get'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        u_id: dict = get_user_id(email, password)
        if u_id is None:
            flash('No account registered for that email')
            return redirect('login')

        session_id = open_session(u_id)

        resp: Response = make_response(redirect(url_for('login')))
        resp.set_cookie('s_id', session_id)
    else:
        resp = make_response(render_template('login.html'))
    return resp


@app.route('/create', methods=['post'])
def create_user():
    print(request.form)
    email = request.form['email']
    password = request.form['password']
    conn = get_db()
    cursor = conn.cursor()
    res = cursor.execute('SELECT * FROM users WHERE email=?', (email, ))
    if res:
        flash('User already exists')
        resp = make_response(redirect('login'))
        return resp
    else:
        cursor.execute('INSERT INTO users (email, password) values (?,?)')




@app.route('/club/<club_id>')
def get_club(club_id):
    pass


if __name__ == '__main__':
    app.secret_key="test"
    app.run(port=8080, debug=True)
