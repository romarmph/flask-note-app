from flask import Blueprint, render_template

web = Blueprint('web', __name__)


@web.route('/about')
def about():
    return render_template("about.html")

@web.route('/management')
def management():
    return render_template("management.html")
