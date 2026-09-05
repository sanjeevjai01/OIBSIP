import requests
from dotenv import load_dotenv
import os
load_dotenv()

api_key = os.getenv("API_KEY")
# -----------------------------
# WEATHER APP
# -----------------------------

print("================================")
print("        WEATHER APP")
print("================================")


# Ask user for city
city = input("Enter city name or ZIP code: ").strip()


# Check empty input
if not city:
    print("Error: City name or ZIP code cannot be empty.")
    exit()



# OpenWeatherMap API URL
url = "https://api.openweathermap.org/data/2.5/weather"


# Parameters for API request
params = {
    "q": city,
    "appid": api_key,
    "units": "metric"
}


try:

    # Send request to OpenWeatherMap
    response = requests.get(url, params=params, timeout=10)


    # -----------------------------
    # ERROR HANDLING
    # -----------------------------

    if response.status_code == 404:
        print("Error: City not found.")

    elif response.status_code == 401:
        print("Error: Invalid API key or API key is not activated yet.")

    elif response.status_code == 200:

        # Convert API response into JSON
        data = response.json()


        # -----------------------------
        # GET WEATHER INFORMATION
        # -----------------------------

        temperature_c = data["main"]["temp"]

        # Celsius to Fahrenheit
        temperature_f = (temperature_c * 9 / 5) + 32

        humidity = data["main"]["humidity"]

        condition = data["weather"][0]["description"]

        wind_speed = data["wind"]["speed"]

        city_name = data["name"]


        # -----------------------------
        # DISPLAY WEATHER
        # -----------------------------

        print("\n================================")
        print("          WEATHER REPORT")
        print("================================")

        print("City          :", city_name)
        print("Temperature   :", temperature_c, "°C")
        print("Temperature   :", round(temperature_f, 2), "°F")
        print("Humidity      :", humidity, "%")
        print("Condition     :", condition.title())
        print("Wind Speed    :", wind_speed, "m/s")

        print("================================")


    else:
        print("Error: Something went wrong.")
        print("Status Code:", response.status_code)


# Network error / timeout
except requests.exceptions.Timeout:

    print("Error: Network timeout. Please try again.")


except requests.exceptions.ConnectionError:

    print("Error: Could not connect to the internet.")


except requests.exceptions.RequestException:

    print("Error: Unable to fetch weather data.")