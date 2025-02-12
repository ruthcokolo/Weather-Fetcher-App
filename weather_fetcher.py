
"""
This script implements a weather-fetching application using PyQt5. 
It includes GUI components, background threading, API interaction, 
and a periodic weather update feature.
"""

import sys
import requests
from functools import lru_cache
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit
from PyQt5.QtCore import QThread, pyqtSignal
import threading
import time
import cProfile


class WeatherFetcherThread(QThread):
    """
    Thread class to fetch weather data in the background.

    Attributes:
        city (str): The city for which weather data will be fetched.
    Signals:
        weather_fetched (pyqtSignal): Emits the weather data upon successful fetch.
        error_occurred (pyqtSignal): Emits an error message if fetching fails.
    """
    weather_fetched = pyqtSignal(dict)
    error_occurred = pyqtSignal(str)

    def __init__(self, city):
        """
        Initializes the WeatherFetcherThread with the specified city.
        
        Args:
            city (str): The name of the city.
        """
        super().__init__()
        self.city = city

    def run(self):
        """
        Executes the weather fetching in a separate thread and emits appropriate signals.
        """
        try:
            data = fetch_weather(self.city)
            self.weather_fetched.emit(data)
        except Exception as e:
            self.error_occurred.emit(str(e))


@lru_cache(maxsize=5)
def fetch_weather(city):
    """
    Fetches weather data for the specified city using the OpenWeatherMap API.

    Args:
        city (str): The name of the city.

    Returns:
        dict: JSON data containing weather details.

    Raises:
        Exception: If the API response is not successful.
    """
    api_key = "d6728ec66d90f2a4876e5637746e6b18" #this is where the OpenWeatherMap API key is entered
    url = f"https://api.openweathermap.org/data/2.5/weather?q={city}&appid={api_key}&units=metric"

    response = requests.get(url, timeout=5)
    if response.status_code != 200:
        raise Exception(f"API Error: {response.status_code} - {response.text}")
    return response.json()


class WeatherApp(QWidget):
    """
    PyQt5 GUI for the Weather Fetcher application.

    Methods:
        fetch_weather(): Initiates weather fetching in a background thread.
        display_weather(data): Updates the GUI with weather information.
        display_error(error): Displays error messages in the GUI.
    """
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Weather Fetcher")
        self.layout = QVBoxLayout()

        self.city_input = QLineEdit()
        self.city_input.setPlaceholderText("Enter city name")
        self.layout.addWidget(self.city_input)

        self.fetch_button = QPushButton("Fetch Weather")
        self.fetch_button.clicked.connect(self.fetch_weather)
        self.layout.addWidget(self.fetch_button)

        self.result_label = QLabel("")
        self.layout.addWidget(self.result_label)

        self.setLayout(self.layout)

    def fetch_weather(self):
        """
        Initiates weather fetching in a background thread.
        """
        city = self.city_input.text()
        if not city:
            self.result_label.setText("Please enter a city name.")
            return

        self.result_label.setText("Fetching weather...")
        self.thread = WeatherFetcherThread(city)
        self.thread.weather_fetched.connect(self.display_weather)
        self.thread.error_occurred.connect(self.display_error)
        self.thread.start()

    def display_weather(self, data):
        """
        Updates the GUI with weather information.

        Args:
            data (dict): JSON data containing weather details.
        """
        weather = data['weather'][0]['description']
        temp = data['main']['temp']
        humidity = data['main']['humidity']
        self.result_label.setText(
            f"Weather: {weather}\nTemperature: {temp}°C\nHumidity: {humidity}%"
        )

    def display_error(self, error):
        """
        Displays errors in the GUI.

        Args:
            error (str): The error message.
        """
        self.result_label.setText(f"Error: {error}")


def periodic_fetcher(city, interval=60):
    """
    Periodically fetches weather data every `interval` seconds in a separate thread.

    Args:
        city (str): The name of the city.
        interval (int): Time interval between fetches in seconds. Default is 60 seconds.
    """
    def fetch():
        while True:
            try:
                data = fetch_weather(city)
                print(f"Periodic Weather Update: {data}")
            except Exception as e:
                print(f"Periodic Fetch Error: {e}")
            time.sleep(interval)

    thread = threading.Thread(target=fetch, daemon=True)
    thread.start()


if __name__ == "__main__":
    """
    Main entry point for the application. Sets up profiling and launches the GUI.
    """
    # Start profiling
    profiler = cProfile.Profile()
    profiler.enable()

    # Launch the PyQt5 GUI
    app = QApplication(sys.argv)
    weather_app = WeatherApp()
    weather_app.show()

    # Example of periodic fetching
    periodic_fetcher("Saskatoon", interval=300)

    # Stop profiling and print results
    exit_code = app.exec_()
    profiler.disable()
    profiler.print_stats(sort="time")
    sys.exit(exit_code)
