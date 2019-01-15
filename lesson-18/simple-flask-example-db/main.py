from flask import Flask
from models import User

app = Flask(__name__)


@app.route("/")
def hello():
    user = User(name="Matt")
    user.create()

    return "Hello, {}!".format(user.name)


if __name__ == '__main__':
    app.run()
