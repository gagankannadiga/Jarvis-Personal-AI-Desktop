import speech_recognition as sr
import pyttsx3
import os
import webbrowser
import datetime
import time
import pyautogui
import smtplib
from email.message import EmailMessage
from playsound import playsound
import cv2
import PyPDF2
import openai
import requests
import pywhatkit as kit
import screen_brightness_control as sbc
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
from openai_api import fetch_info_from_openai
import psutil
import pyjokes
import subprocess
import threading
import keyboard
import pygame
import communication
import utilities
import music_player
import tkinter as tk
from PIL import Image, ImageTk
import time

# Initialize Text-to-Speech
engine = pyttsx3.init()

# Initialize pygame mixer
pygame.mixer.init()

# Initialize pygame only once
pygame.init()

# Configuration
engine = pyttsx3.init()
conversation_history = ""
webcam_active = False
alarm_path = r"C:\Users\Chandrashekhar B N\Downloads\Ultra Kwangsoo Tarararara Ringtone - MobCup.Com.Co.mp3"

# Functions
def say(text):
    engine.say(text)
    engine.runAndWait()
    print(text)

#Greet User
def greet_user():
    """Greets the user based on the time of day and asks how they're doing."""
    current_hour = datetime.datetime.now().hour
    if current_hour < 12:
        greeting = "Good morning!"
    elif 12 <= current_hour < 18:
        greeting = "Good afternoon!"
    else:
        greeting = "Good evening!"

    say(f"{greeting} How are you today?")
    response = take_command()
    if response:
        if "good" in response or "fine" in response:
            say("I'm glad to hear that! How can I assist you today?")
        elif "not" in response or "bad" in response:
            say("I'm sorry to hear that. I hope I can help make your day better. What can I do for you?")
        else:
            say("Alright! How can I assist you today?")
    else:
        say("I didn't catch that. How can I assist you today?")

# Take command function
def take_command():
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening...")
        recognizer.pause_threshold = 2  # Allow longer pauses during dictation
        audio = recognizer.listen(source)
        try:
            print("Recognizing...")
            command = recognizer.recognize_google(audio, language="en-in")
            print(f"User said: {command}")
            return command.lower()
        except Exception:
            print("Could not understand. Please try again.")
            return ""

#To fetch information from api
def fetch_info_from_openai(query):
    global conversation_history
    try:
        conversation_history += f"User: {query}\n"
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "You are an AI assistant."},
                {"role": "user", "content": query}
            ],
            max_tokens=200,
            temperature=0.7
        )
        answer = response["choices"][0]["message"]["content"].strip()
        conversation_history += f"Jarvis: {answer}\n"
        return answer
    except Exception as e:
        return f"Error fetching answer: {e}"

#Adjust Brightness
def adjust_brightness(action):
    try:
        current_brightness = sbc.get_brightness()[0]
        if "increase" in action:
            sbc.set_brightness(min(current_brightness + 20, 100))
            say("Increasing brightness.")
        elif "decrease" in action:
            sbc.set_brightness(max(current_brightness - 20, 0))
            say("Decreasing brightness.")
        else:
            say("Brightness adjustment command not understood.")
    except Exception as e:
        print(f"Error: {e}")
        say("Unable to adjust brightness.")

#Adjust Volume
def adjust_volume(action):
    try:
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        volume = cast(interface, POINTER(IAudioEndpointVolume))
        current_volume = volume.GetMasterVolumeLevelScalar()

        if "increase" in action:
            volume.SetMasterVolumeLevelScalar(min(current_volume + 0.1, 1.0), None)
            say("Increasing volume.")
        elif "decrease" in action:
            volume.SetMasterVolumeLevelScalar(max(current_volume - 0.1, 0.0), None)
            say("Decreasing volume.")
        else:
            say("Volume adjustment command not understood.")
    except Exception as e:
        print(f"Error: {e}")
        say("Unable to adjust volume.")

#Open and Close Webcam
def open_close_webcam(action):
    global webcam_active
    if "open" in action:
        webcam_active = True
        cap = cv2.VideoCapture(0)
        say("Webcam opened. Say 'capture' to take a photo.")
        while webcam_active:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture video.")
                break
            cv2.imshow('Webcam', frame)
            if cv2.waitKey(1) & 0xFF == ord('q') or not webcam_active:
                break
            elif take_command() == "capture":
                cv2.imwrite("photo.png", frame)
                say("Photo captured and saved.")
        cap.release()
        cv2.destroyAllWindows()
    elif "close" in action:
        webcam_active = False
        say("Webcam closed.")


#Sing a song
songs = [
    {
        "title": "Shape of You",
        "artist": "Ed Sheeran",
        "lyrics": [
            "The club isn't the best place to find a lover,",
            "So the bar is where I go.",
            "Me and my friends at the table doing shots,",
            "Drinking fast and then we talk slow."
        ]
    },
    {
        "title": "Blinding Lights",
        "artist": "The Weeknd",
        "lyrics": [
            "I said, ooh, I'm blinded by the lights,",
            "No, I can't sleep until I feel your touch.",
            "I said, ooh, I'm drowning in the night,",
            "Oh, when I'm like this, you're the one I trust."
        ]
    },
    {
        "title": "Levitating",
        "artist": "Dua Lipa",
        "lyrics": [
            "If you wanna run away with me, I know a galaxy,",
            "And I can take you for a ride.",
            "I had a premonition that we fell into a rhythm,",
            "Where the music don't stop for life."
        ]
    }
]

song_index = 0  # Keeps track of the last song played

def sing_a_song():
    """Makes Jarvis sing a song from a list of modern songs."""
    global song_index

    # Select the current song based on the song_index
    song = songs[song_index]
    say(f"Alright, here's {song['title']} by {song['artist']}. Enjoy!")

    # Sing the song lyrics
    for line in song["lyrics"]:
        say(line)

    # Move to the next song, wrapping around the list if needed
    song_index = (song_index + 1) % len(songs)

def play_song():
    """Triggers the music player to play the next song."""
    music_player.play_next_song()

def stop_song():
    """Stops the currently playing song."""
    music_player.stop_song()

#Detect Weather
def show_image(image_path):
    """Displays the image in a separate Tkinter window."""
    root = tk.Toplevel()  # Create a separate window
    root.title("Weather Forecast")

    img = Image.open(image_path)
    img = img.resize((800, 600), Image.LANCZOS)  # Increased image size
    img = ImageTk.PhotoImage(img)

    label = tk.Label(root, image=img)
    label.image = img  # Keep reference to prevent garbage collection
    label.pack()

    root.geometry("800x600")  # Match the image size
    root.update()

    return root  # Return the window object to close it later


def detect_weather(city):
    """Fetches weather information and displays an image during processing."""
    api_key = "782e6b248f3ad1264a2ebd44905cbc91"  # Replace with your OpenWeather API key
    url = f"http://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    image_path = r"C:\Users\Chandrashekhar B N\Desktop\Jarvis Screensots\Screenshot 2025-02-01 204119.png"

    try:
        # Show the weather forecast image
        img_window = show_image(image_path)

        # Fetch weather data
        response = requests.get(url)
        weather_data = response.json()
        print(weather_data)  # Debugging: Print API response

        if response.status_code == 200:  # Ensure API request was successful
            temperature = weather_data["main"]["temp"]
            weather_desc = weather_data["weather"][0]["description"]
            result = f"The temperature in {city} is {temperature} degrees Celsius with {weather_desc}."
        else:
            result = "City not found."

        say(result)

        # Close the image window after responding
        img_window.destroy()

    except Exception as e:
        print(f"Error: {e}")
        say("Unable to fetch weather information.")



#Send Email
def send_email():
    try:
        say("Please type the receiver's email address:")
        receiver_email = input("Enter receiver email address: ")
        say("What should I say in the email?")
        content = take_command()

        sender_email = "yashwanthgowdabc97@gmail.com"  # Replace with your email
        sender_password = "xnql ldim wxuq zpxw"  # Replace with your app password

        msg = EmailMessage()
        msg.set_content(content)
        msg['Subject'] = "Email from Jarvis"
        msg['From'] = sender_email
        msg['To'] = receiver_email

        server = smtplib.SMTP('smtp.gmail.com', 587)
        server.starttls()
        server.login(sender_email, sender_password)
        server.send_message(msg)
        server.quit()

        say("Email sent successfully.")
    except Exception as e:
        print(f"Error: {e}")
        say("Unable to send the email.")

#Crack Jokes
def crack_joke():
    """Tells a joke."""
    joke = pyjokes.get_joke(language="en", category="neutral")
    say(f"Here's a joke for you: {joke}")

#Search on Google
def search_google():
    say("What should I search on Google?")
    query = take_command()
    if query:
        url = f"https://www.google.com/search?q={query}"
        webbrowser.open(url)
        say(f"Searching Google for {query}.")

#Play on YouTube
def play_on_youtube():
    """Plays a requested video on YouTube."""
    say("What video would you like to play on YouTube?")
    command = take_command()
    if command:
        say(f"Playing {command} on YouTube.")
        kit.playonyt(command)
    else:
        say("I couldn't hear your request.")

#open and close system settings
def open_close_system_app(action, app):
    try:
        if "open" in action:
            say(f"Opening {app}.")
            if app == "settings":
                subprocess.run("start ms-settings:", shell=True)
            else:
                os.system(f"start {app}")
        elif "close" in action:
            say(f"Closing {app}.")
            if app == "settings":
                subprocess.run("taskkill /im SystemSettings.exe /f", shell=True)
            else:
                # Added a short delay to ensure the app is running before trying to kill it
                time.sleep(1)
                subprocess.run(f"taskkill /im {app}.exe /f", shell=True)
                # Optionally, check if the process is still running
                time.sleep(1)
                if is_process_running(app):
                    say(f"Could not close {app}.")
                else:
                    say(f"{app} closed successfully.")
    except Exception as e:
        print(f"Error: {e}")
        say(f"Unable to handle {app}.")


def is_process_running(app_name):
    # Check if the process is still running by looking for the app's executable
    result = subprocess.run(f"tasklist /FI \"IMAGENAME eq {app_name}.exe\"", capture_output=True, text=True, shell=True)
    return app_name in result.stdout


#Check Battery Status
def get_battery_status():
    battery = psutil.sensors_battery()
    if battery:
        percent = battery.percent
        plugged = "plugged in" if battery.power_plugged else "not plugged in"
        say(f"Your battery is at {percent} percent and it is {plugged}.")
    else:
        say("Unable to fetch battery information.")

#Set Alarm
def set_alarm(alarm_time, alarm_sound):
    """Set an alarm and stop it when 'q' is pressed."""
    try:
        # Parse the time and convert it to 24-hour format
        alarm_time = alarm_time.strip().replace("a.m.", "AM").replace("p.m.", "PM").replace("am", "AM").replace("pm",
                                                                                                                "PM")
        if "AM" in alarm_time or "PM" in alarm_time:
            alarm_datetime = datetime.datetime.strptime(alarm_time, "%I:%M %p")
        else:
            alarm_datetime = datetime.datetime.strptime(alarm_time, "%H:%M")

        alarm_hour = alarm_datetime.hour
        alarm_minute = alarm_datetime.minute

        print(f"Alarm set for {alarm_time}. Press 'q' to stop the alarm once it rings.")

        # Wait for the alarm time
        while True:
            now = datetime.datetime.now()
            if now.hour == alarm_hour and now.minute == alarm_minute:
                print("Time to wake up!")
                break
            time.sleep(30)

        # Play the alarm sound
        pygame.mixer.music.load(alarm_sound)
        pygame.mixer.music.play(-1)  # Loop the alarm sound indefinitely

        # Wait for 'q' key to stop the alarm
        while True:
            if keyboard.is_pressed("q"):
                print("Stopping alarm...")
                pygame.mixer.music.stop()  # Stop the alarm sound
                print("Alarm stopped.")
                break

    except Exception as e:
        print(f"Error: {e}")
        print("Sorry, I couldn't set the alarm.")

# Shutdown function
def shutdown_system():
    """Shuts down the system."""
    say("Are you sure you want me to shut down the system? Please confirm.")
    confirmation = take_command()
    if "yes" in confirmation or "confirm" in confirmation:
        say("Shutting down the system. Goodbye!")
        os.system("shutdown /s /t 5")  # Shutdown command for Windows
    else:
        say("Shutdown canceled.")

import threading
import gui  # Import the GUI module

#Main Program
def run_jarvis():
    say("Jarvis is now online.")
    greet_user()

    while True:
        query = take_command()

        if "increase brightness" in query:
            adjust_brightness("increase")
        elif "decrease brightness" in query:
            adjust_brightness("decrease")
        elif "increase volume" in query:
            adjust_volume("increase")
        elif "decrease volume" in query:
            adjust_volume("decrease")
        elif "open webcam" in query or "close webcam" in query:
            open_close_webcam(query)
        elif "take notes" in query:
            utilities.take_notes()
        elif "take a screenshot" in query or "screenshot" in query:
            utilities.take_screenshot()
        elif "detect weather" in query:
            say("Please specify the city.")
            city = take_command()
            detect_weather(city)
        elif "send email" in query:
            send_email()
        elif "crack a joke" in query:
            crack_joke()
        elif "shutdown" in query:
            shutdown_system()
        elif "send whatsapp message" in query:
            communication.send_whatsapp_message()
        elif "make a phone call" in query:
            communication.make_phone_call()
        elif "search on google" in query:
            search_google()
        elif "play on youtube" in query:
            play_on_youtube()
        elif "battery status" in query:
            get_battery_status()
        elif "sing me a song" in query:
            sing_a_song()
        elif "play a song" in query:
            play_song()
        elif "stop music" in query or "stop song" in query:
            stop_song()
        elif "set alarm" in query:
            say("Please type the time for the alarm in HH:MM format or specify AM/PM.")
            alarm_time = input("Enter the alarm time: ")
            set_alarm(alarm_time, alarm_path)
        elif "open paint" in query or "close paint" in query:
            open_close_system_app(query, "mspaint")
        elif "open notepad" in query or "close notepad" in query:
            open_close_system_app(query, "notepad")
        elif "open settings" in query or "close settings" in query:
            open_close_system_app(query, "settings")
        elif "quit" in query or "exit" in query:
            say("Goodbye Boss!")
            break
        else:
            answer = fetch_info_from_openai(query)
            say(answer)
            print(f"Jarvis: {answer}")

if __name__ == "__main__":
    # Start GUI in a separate thread
    gui_thread = threading.Thread(target=gui.start_gui, daemon=True)
    gui_thread.start()
    # Start voice assistant logic in the main thread
    run_jarvis()

