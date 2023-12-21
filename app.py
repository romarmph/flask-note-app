from functools import wraps
from flask import Flask, render_template
from pymysql import OperationalError
from sqlalchemy import text
from routes.web import web
from db import db, init_app

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/flask_notes'

init_app(app)

app.secret_key = "mysecretkey"
app.register_blueprint(web)


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html")


@app.route('/test_db')
def test_db():
    try:
        result = db.session.execute(text('SELECT * FROM users')).fetchall()
        # Fetch all rows from the result (optional)
        return 'Success! Connected to the database.'
    except OperationalError:
        return 'Error! Could not connect to the database.'


if __name__ == '__main__':
    app.run(debug=True)
