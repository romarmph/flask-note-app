from functools import wraps
from flask import Blueprint, redirect, render_template, request, session, url_for, flash

from db import db


class Users(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    created_at = db.Column(db.DateTime, nullable=False)


web = Blueprint('web', __name__)


@web.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if username or password are empty
        if not username:
            flash('Username is required.')
            return render_template("login.html")
        if not password:
            flash('Password is required.')
            return render_template("login.html")

        user = Users.query.filter_by(username=username).first()

        # Check if username is incorrect
        if not user:
            flash('Incorrect Username.')
            return render_template("login.html")

        # Check if password is incorrect
        if user.password != password:
            flash('Incorrect Password.')
            return render_template("login.html")

        session['username'] = username
        next_page = request.args.get('next', url_for('web.index'))
        return redirect(next_page)

    return render_template("login.html")


@web.route('/logout')
def logout():
    session.pop('username', None)
    return redirect(url_for('web.login'))


def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'username' not in session:
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated_function


@web.route("/")
@web.route("/index")
@login_required
def index():
    return render_template("index.html")


@web.route('/about')
@login_required
def about():
    return render_template("about.html")


@web.route('/management')
@login_required
def management():
    return render_template("management.html")
