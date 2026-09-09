import sys
import subprocess
import datetime
import webbrowser

import pyaudiowpatch as pyaudio
sys.modules["pyaudio"] = pyaudio

import speech_recognition as sr

# TEXT TO SPEECH

def speak(text):
    print("Assistant:", text)

    tts_code = f"""
import pyttsx3

engine = pyttsx3.init("sapi5")

engine.setProperty("rate", 200)
engine.setProperty("volume", 1.0)

engine.say({text!r})
engine.runAndWait()
engine.stop()
"""

    try:
        subprocess.run(
            [sys.executable, "-c", tts_code],
            check=True
        )
    except Exception as error:
        print("TTS Error:", error)


# VOICE INPUT
recognizer = sr.Recognizer()

recognizer.energy_threshold = 300
recognizer.dynamic_energy_threshold = True
recognizer.pause_threshold = 0.7
recognizer.non_speaking_duration = 0.4


def listen():
    with sr.Microphone() as source:

        print("Listening...")

        try:
            audio = recognizer.listen(
                source,
                timeout=None,
                phrase_time_limit=None
            )
        except Exception as error:
            print("Microphone Error:", error)
            return ""

    try:
        command = recognizer.recognize_google(
            audio,
            language="en-IN"
        )

        command = command.lower().strip()

        print("You:", command)

        return command

    except sr.UnknownValueError:
        print("Could not understand.")
        return ""

    except sr.RequestError:
        speak("Sorry, I cannot connect to the speech recognition service.")
        return ""



# MAIN
def main():

    print("=" * 50)
    print("       BASIC VOICE ASSISTANT")
    print("=" * 50)

    print("Commands:")
    print("Hello")
    print("What is the time")
    print("What is today's date")
    print("What day is today")
    print("Open Google")
    print("Open YouTube")
    print("Bye / Stop / Exit")
    print("=" * 50)

    # Microphone calibration
    print("\nCalibrating microphone...")

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(
            source,
            duration=1
        )

    print("Microphone ready.")

    speak("Hello Sanjeev. I am your voice assistant.")

    while True:

        command = listen()

        if not command:
            continue

        # ==========================
        # STOP / BYE
        # ==========================
        if (
            command == "bye"
            or command == "goodbye"
            or command == "stop"
            or command.startswith("bye ")
            or command.startswith("goodbye ")
            or command.startswith("stop ")
            or " bye" in command
            or " goodbye" in command
            or " stop" in command
        
        ):
            speak("Goodbye Sanjeev.")
            print("Assistant stopped.")
            break

        # ==========================
        # GREETING
        # ==========================
        elif (
            "hello" in command
            or "hi" in command
            or "hey" in command
        ):
            speak("Hello Sanjeev. How can I help you?")

        # ==========================
        # TIME
        # ==========================
        elif (
            "what time" in command
            or "what is the time" in command
            or "tell me the time" in command
            or command == "time"
        ):
            current_time = datetime.datetime.now().strftime(
                "%I:%M %p"
            )

            speak(f"The current time is {current_time}.")

        # ==========================
        # DATE
        # ==========================
        elif (
            "today's date" in command
            or "todays date" in command
            or "what is the date" in command
            or "tell me the date" in command
            or command == "date"
        ):
            current_date = datetime.datetime.now().strftime(
                "%A, %B %d, %Y"
            )

            speak(f"Today is {current_date}.")

        # ==========================
        # DAY
        # ==========================
        elif (
            "what day is today" in command
            or "what day is it" in command
            or "which day is today" in command
            or command == "day"
        ):
            current_day = datetime.datetime.now().strftime(
                "%A"
            )

            speak(f"Today is {current_day}.")

        # ==========================
        # GOOGLE
        # ==========================
        elif (
            "open google" in command
            or command == "google"
        ):
            speak("Opening Google.")
            webbrowser.open("https://www.google.com")

        # ==========================
        # YOUTUBE
        # ==========================
        elif (
            "open youtube" in command
            or command == "youtube"
        ):
            speak("Opening YouTube.")
            webbrowser.open("https://www.youtube.com")

        # ==========================
        # UNKNOWN COMMAND
        # ==========================
        else:
            speak("Sorry, I did not understand that command.")


# ==============================
# START PROGRAM
# ==============================
if __name__ == "__main__":
    main()