import requests
from flask import Flask, render_template

app = Flask(__name__)


@app.route("/", methods=["GET"])
def index():
    query = "London,UK"
    unit = "metric"  # use "imperial" for Fahrenheit or "kelvin" for degrees Kelvin
    api_key = "7227ec42d0eaa974ef8bede8141ff4ec"  # DO NOT UPLOAD YOUR KEY TO GITHUB. Use env var instead: os.environ.get("OWM_KEY")

    url = "https://api.openweathermap.org/data/2.5/weather?q={0}&units={1}&appid={2}".format(query, unit, api_key)

    data = requests.get(url=url)  # GET request to the OpenWeatherMap API

    print(data.text)

    return render_template("index.html", data=data.json())


if __name__ == '__main__':
    app.run(debug=True)
