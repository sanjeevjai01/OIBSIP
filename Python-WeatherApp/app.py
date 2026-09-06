from flask import Flask, render_template, request
import requests
from dotenv import load_dotenv
import os

load_dotenv()

app = Flask(__name__)

API_KEY = os.getenv("API_KEY")


@app.route("/", methods=["GET", "POST"])
def home():

    weather = None
    error = None

    if request.method == "POST":

        city = request.form.get("city", "").strip()

        if not city:
            error = "Please enter a city name."
        else:

            url = "https://api.openweathermap.org/data/2.5/weather"

            params = {
                "q": city,
                "appid": API_KEY,
                "units": "metric"
            }

            try:

                response = requests.get(
                    url,
                    params=params,
                    timeout=10
                )

                if response.status_code == 404:
                    error = "City not found."

                elif response.status_code == 401:
                    error = "Invalid API key or API key is not activated yet."

                elif response.status_code == 200:

                    data = response.json()

                    temperature_c = data["main"]["temp"]
                    temperature_f = (temperature_c * 9 / 5) + 32

                    weather = {
                        "city": data["name"],
                        "country": data["sys"]["country"],
                        "temperature_c": temperature_c,
                        "temperature_f": round(temperature_f, 2),
                        "humidity": data["main"]["humidity"],
                        "condition": data["weather"][0]["description"].title(),
                        "wind": data["wind"]["speed"]
                    }

                else:
                    error = "Something went wrong."

            except requests.exceptions.Timeout:
                error = "Network timeout. Please try again."

            except requests.exceptions.ConnectionError:
                error = "Could not connect to the internet."

            except requests.exceptions.RequestException:
                error = "Unable to fetch weather data."

    return render_template(
        "index.html",
        weather=weather,
        error=error
    )


if __name__ == "__main__":
    app.run(debug=True)