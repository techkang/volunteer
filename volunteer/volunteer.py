# -*- coding:utf-8 -*-
# all the imports
import os
import sqlite3
from flask import Flask, request, session, g, redirect, url_for, abort, \
    render_template, flash

app = Flask(__name__)  # create the application instance :)
app.config.from_object(__name__)  # load config from this file , flaskr.py

# Load default config and override config from an environment variable
app.config.update(dict(
    DATABASE=os.path.join(app.root_path, 'volunteer.db'),
    SECRET_KEY='thisisarandomkey',
    USERNAME='admin',
    PASSWORD='default'
))
app.config.from_envvar('VOLUNTEER_SETTINGS', silent=True)


def connect_db():
    """Connects to the specific database."""
    rv = sqlite3.connect(app.config['DATABASE'])
    rv.row_factory = sqlite3.Row
    return rv


def init_db():
    db = get_db()
    with app.open_resource('schema.sql', mode='r') as f:
        db.cursor().executescript(f.read())
    db.commit()


@app.cli.command('initdb')
@app.route('/initdb')
def initdb_command():
    """Initializes the database."""
    init_db()
    print('Initialized the database.')
    render_template('index.html')


def get_db():
    """Opens a new database connection if there is none yet for the
    current application context.
    """
    if not hasattr(g, 'sqlite_db'):
        g.sqlite_db = connect_db()
    return g.sqlite_db


@app.teardown_appcontext
def close_db(error):
    """Closes the database again at the end of the request."""
    if hasattr(g, 'sqlite_db'):
        g.sqlite_db.close()


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/login')
def login():
    return render_template('login.html')


@app.route('/summer', methods=['GET', 'POST'])
def summer():
    return "报名尚未开放，感谢关注！"
    error = None
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'insert into entries (stdnum,name,province,school,last_exam,sex,email,phone,info) values (?,?,?,?,?,?,?,?,?)',
            [request.form['stdnum'], request.form['name'], request.form['province'], request.form['school'],
             request.form['last_exam'], request.form['sex'], request.form['email'], request.form['phone'],
             request.form['info']])
        db.commit()
        flash('New student successfully registered!')
        return redirect(url_for('finish'))
    return render_template('summer.html', error=error)


@app.route('/winter', methods=['GET', 'POST'])
def winter():
    return "报名尚未开放，感谢关注！"
    error = None
    if request.method == 'POST':
        db = get_db()
        db.execute(
            'insert into entries (stdnum,name,province,school,last_exam,sex,email,phone,info) values (?,?,?,?,?,?,?,?,?)',
            [request.form['stdnum'], request.form['name'], request.form['province'], request.form['school'],
             request.form['last_exam'], request.form['sex'], request.form['email'], request.form['phone'],
             request.form['info']])
        db.commit()
        flash('New student successfully registered!')
        return redirect(url_for('finish'))
    return render_template('winter.html', error=error)


@app.route('/new', methods=['GET', 'POST'])
def new():
    error = None
    flag = 0
    if request.method == 'POST':
        db = get_db()
        if len(request.form['stdnum']) != 10:
            error = 'The length of student number should be 10!'
            flag = 1
        elif len(request.form['phone']) != 11:
            error = 'The length of phone number should be 11'
            flag = 1
        elif len(request.form['info']) < 10:
            error = 'The length of person information should be 10'
            flag = 1
        if flag == 0:
            db.execute('insert into entries (stdnum,name,sex,email,phone,info) values (?,?,?,?,?,?)',
                       [request.form['stdnum'], request.form['name'], request.form['sex'], request.form['email'],
                        request.form['phone'], request.form['info']])
            db.commit()
            flash('New student successfully registered!')
            return redirect(url_for('finish'))
    return render_template('new.html', error=error)


@app.route('/finish')
def finish():
    return render_template('finish.html')


@app.route('/manager', methods=['GET', 'POST'])
def manager():
    error = None
    if request.method == 'POST':
        if request.form['username'] != app.config['USERNAME'] or \
                        request.form['password'] != app.config['PASSWORD']:
            # error='用户名或密码错误！'
            error = 'Invalid username or password!'
        else:
            session['logged_in'] = True
            flash('You were logged in')
            return redirect(url_for('show_entries'))
    return render_template('manager.html', error=error)


@app.route('/show_entries')
def show_entries():
    if not session.get('logged_in'):
        abort(401)
    db = get_db()
    cur = db.execute('select stdnum, name, sex, info from entries order by id desc')
    entries = cur.fetchall()
    return render_template('show_entries.html', entries=entries)


@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    flash('You were logged out')
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run( debug=True)
