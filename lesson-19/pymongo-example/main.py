from flask import Flask, render_template, request, redirect, url_for, make_response
from models import User

app = Flask(__name__)


@app.route("/")
def index():
    email_address = request.cookies.get("email")

    if email_address:
        user = User.get_collection().find_one({"email": email_address})
    else:
        user = None

    return render_template("index.html", user=user)


@app.route("/login", methods=["POST"])
def login():
    name = request.form.get("user-name")
    email = request.form.get("user-email")

    # create a user object
    user = User(name=name, email=email)

    # insert the user object into the User collection
    User.get_collection().insert_one(user.__dict__)

    # save user's email into a cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


if __name__ == '__main__':
    app.run()
