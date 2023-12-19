from flask import Flask, render_template
from routes.web import web

app = Flask(__name__)
app.register_blueprint(web)


@app.route("/")
@app.route("/index")
def index():
    return render_template("index.html")


@app.errorhandler(404)
def page_not_found(e):
    return render_template("error/404.html")


if __name__ == '__main__':
    app.run(debug=True)
