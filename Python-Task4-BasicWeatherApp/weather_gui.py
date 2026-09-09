import tkinter as tk
from tkinter import messagebox
import requests
from dotenv import load_dotenv
import os

# Load API key
load_dotenv()
API_KEY = os.getenv("API_KEY")


# -----------------------------
# WEATHER FUNCTION
# -----------------------------
def get_weather():
    city = city_entry.get().strip()

    if city == "" or city == "Enter city name or ZIP code":
        messagebox.showerror(
            "Input Error",
            "Please enter a city name or ZIP code."
        )
        return

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
            messagebox.showerror(
                "City Not Found",
                "The city you entered was not found."
            )
            return

        if response.status_code == 401:
            messagebox.showerror(
                "API Error",
                "Invalid API key or API key is not activated yet."
            )
            return

        if response.status_code != 200:
            messagebox.showerror(
                "Error",
                f"Something went wrong.\nStatus Code: {response.status_code}"
            )
            return

        data = response.json()

        city_name = data["name"]
        country = data["sys"]["country"]

        temperature_c = data["main"]["temp"]
        temperature_f = (temperature_c * 9 / 5) + 32

        humidity = data["main"]["humidity"]
        condition = data["weather"][0]["description"].title()
        wind_speed = data["wind"]["speed"]

        # Update city name
        location_label.config(
            text=f"📍 {city_name}, {country}"
        )

        # Update temperature
        temperature_label.config(
            text=f"{temperature_c:.1f}°C"
        )

        fahrenheit_label.config(
            text=f"{temperature_f:.1f}°F"
        )

        # Update other information
        condition_value.config(
            text=condition
        )

        humidity_value.config(
            text=f"{humidity}%"
        )

        wind_value.config(
            text=f"{wind_speed} m/s"
        )

        # Show weather card
        weather_card.pack(
            pady=25,
            padx=35,
            fill="x"
        )

    except requests.exceptions.Timeout:
        messagebox.showerror(
            "Network Error",
            "Network timeout. Please try again."
        )

    except requests.exceptions.ConnectionError:
        messagebox.showerror(
            "Network Error",
            "Could not connect to the internet."
        )

    except requests.exceptions.RequestException:
        messagebox.showerror(
            "Error",
            "Unable to fetch weather data."
        )


# -----------------------------
# MAIN WINDOW
# -----------------------------
root = tk.Tk()

root.title("Weather App")
root.geometry("1000x750")
root.minsize(800, 600)
root.resizable(True, True)

# Background
root.configure(bg="#101827")


# -----------------------------
# HEADER
# -----------------------------
header = tk.Frame(
    root,
    bg="#101827"
)

header.pack(
    fill="x",
    pady=(35, 5)
)

title_label = tk.Label(
    header,
    text="🌦 WEATHER APP",
    font=("Segoe UI", 28, "bold"),
    bg="#101827",
    fg="white"
)

title_label.pack()

subtitle_label = tk.Label(
    header,
    text="Real-time weather information",
    font=("Segoe UI", 12),
    bg="#101827",
    fg="#aeb8c7"
)

subtitle_label.pack(
    pady=(5, 0)
)


# -----------------------------
# SEARCH AREA
# -----------------------------
search_frame = tk.Frame(
    root,
    bg="#182235"
)

search_frame.pack(
    padx=35,
    pady=30,
    fill="x"
)

city_entry = tk.Entry(
    search_frame,
    font=("Segoe UI", 15),
    bg="#243148",
    fg="white",
    insertbackground="white",
    relief="flat",
    justify="center"
)

city_entry.pack(
    side="left",
    padx=(15, 10),
    pady=15,
    ipady=10,
    fill="x",
    expand=True
)

city_entry.insert(
    0,
    "Enter city name or ZIP code"
)


# -----------------------------
# PLACEHOLDER
# -----------------------------
def clear_placeholder(event):
    if city_entry.get() == "Enter city name or ZIP code":
        city_entry.delete(0, tk.END)


def restore_placeholder(event):
    if city_entry.get().strip() == "":
        city_entry.insert(
            0,
            "Enter city name or ZIP code"
        )


city_entry.bind(
    "<FocusIn>",
    clear_placeholder
)

city_entry.bind(
    "<FocusOut>",
    restore_placeholder
)


# -----------------------------
# SEARCH BUTTON
# -----------------------------
search_button = tk.Button(
    search_frame,
    text="SEARCH",
    font=("Segoe UI", 12, "bold"),
    bg="#2563eb",
    fg="white",
    activebackground="#1d4ed8",
    activeforeground="white",
    relief="flat",
    cursor="hand2",
    command=get_weather
)

search_button.pack(
    side="right",
    padx=(0, 15),
    pady=15,
    ipadx=15,
    ipady=8
)


# -----------------------------
# WEATHER CARD
# -----------------------------
weather_card = tk.Frame(
    root,
    bg="#182235"
)

location_label = tk.Label(
    weather_card,
    text="📍 City",
    font=("Segoe UI", 17, "bold"),
    bg="#182235",
    fg="white"
)

location_label.pack(
    pady=(25, 10)
)


temperature_label = tk.Label(
    weather_card,
    text="--°C",
    font=("Segoe UI", 48, "bold"),
    bg="#182235",
    fg="white"
)

temperature_label.pack()


fahrenheit_label = tk.Label(
    weather_card,
    text="--°F",
    font=("Segoe UI", 14),
    bg="#182235",
    fg="#aeb8c7"
)

fahrenheit_label.pack(
    pady=(0, 20)
)


# -----------------------------
# WEATHER DETAILS
# -----------------------------
details_frame = tk.Frame(
    weather_card,
    bg="#182235"
)

details_frame.pack(
    pady=(5, 25)
)


# -----------------------------
# CONDITION
# -----------------------------
condition_box = tk.Frame(
    details_frame,
    bg="#243148"
)

condition_box.grid(
    row=0,
    column=0,
    padx=6,
    pady=5
)

tk.Label(
    condition_box,
    text="☁ Condition",
    font=("Segoe UI", 10),
    bg="#243148",
    fg="#aeb8c7"
).pack(
    pady=(10, 2)
)

condition_value = tk.Label(
    condition_box,
    text="--",
    font=("Segoe UI", 12, "bold"),
    bg="#243148",
    fg="white"
)

condition_value.pack(
    padx=20,
    pady=(0, 10)
)


# -----------------------------
# HUMIDITY
# -----------------------------
humidity_box = tk.Frame(
    details_frame,
    bg="#243148"
)

humidity_box.grid(
    row=0,
    column=1,
    padx=6,
    pady=5
)

tk.Label(
    humidity_box,
    text="💧 Humidity",
    font=("Segoe UI", 10),
    bg="#243148",
    fg="#aeb8c7"
).pack(
    pady=(10, 2)
)

humidity_value = tk.Label(
    humidity_box,
    text="--%",
    font=("Segoe UI", 12, "bold"),
    bg="#243148",
    fg="white"
)

humidity_value.pack(
    padx=20,
    pady=(0, 10)
)


# -----------------------------
# WIND
# -----------------------------
wind_box = tk.Frame(
    details_frame,
    bg="#243148"
)

wind_box.grid(
    row=0,
    column=2,
    padx=6,
    pady=5
)

tk.Label(
    wind_box,
    text="💨 Wind",
    font=("Segoe UI", 10),
    bg="#243148",
    fg="#aeb8c7"
).pack(
    pady=(10, 2)
)

wind_value = tk.Label(
    wind_box,
    text="-- m/s",
    font=("Segoe UI", 12, "bold"),
    bg="#243148",
    fg="white"
)

wind_value.pack(
    padx=20,
    pady=(0, 10)
)


# -----------------------------
# FOOTER
# -----------------------------
footer_label = tk.Label(
    root,
    text="Developed By Sanjeev Kumar Jaiswal",
    font=("Segoe UI", 10),
    bg="#101827",
    fg="#8397B6"
)

footer_label.pack(
    side="bottom",
    pady=18
)


# -----------------------------
# ENTER KEY SUPPORT
# -----------------------------
root.bind(
    "<Return>",
    lambda event: get_weather()
)


# -----------------------------
# START APPLICATION
# -----------------------------
root.mainloop()