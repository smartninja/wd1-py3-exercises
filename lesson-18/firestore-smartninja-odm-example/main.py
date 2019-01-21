from flask import Flask, render_template, request, redirect, url_for, make_response
from models import User

app = Flask(__name__)


@app.route("/")
def index():
    email_address = request.cookies.get("email")

    if email_address:
        query = ["email", "==", email_address]
        users = User.fetch(query=query)
        user = users[0]  # take the first element from the list
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    # create a User object
    user = User(name=name, email=email)
    user.create()  # save the object into a database

    # save user's email into a cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


if __name__ == '__main__':
    app.run()
