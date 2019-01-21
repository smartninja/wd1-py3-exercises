import random
from flask import Flask, render_template, request, make_response, redirect, url_for
from models import User

app = Flask(__name__)


@app.route("/", methods=["GET"])
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

    # create a secret number
    secret_number = random.randint(1, 30)

    # create a user object
    user = User(name=name, email=email, secret_number=secret_number)

    # insert the user object into the User collection
    User.get_collection().insert_one(user.__dict__)

    # save user's email into a cookie
    response = make_response(redirect(url_for('index')))
    response.set_cookie("email", email)

    return response


@app.route("/result", methods=["POST"])
def result():
    guess = int(request.form.get("guess"))

    email_address = request.cookies.get("email")

    if email_address:
        user = User.get_collection().find_one({"email": email_address})
    else:
        return render_template("index.html", user=None)

    if guess == user["secret_number"]:
        message = "Correct! The secret number is {0}".format(str(guess))

        # create a new random secret number
        new_secret = random.randint(1, 30)

        # update the user's secret number in the User collection
        User.get_collection().update_one({"_id": user["_id"]}, {"$set": {"secret_number": new_secret}})
    elif guess > user["secret_number"]:
        message = "Your guess is not correct... try something smaller."
    elif guess < user["secret_number"]:
        message = "Your guess is not correct... try something bigger."

    return render_template("result.html", message=message)


if __name__ == '__main__':
    app.run(debug=True)
