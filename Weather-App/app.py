import requests
import configparser
import datetime
from flask import Flask, render_template, request


app = Flask(__name__)


@app.route('/')
def weather_dashboard():
    return render_template('home.html')


@app.route('/results', methods=['POST'])
def render_results():
    global c_name
    c_name = request.form['city_name']
    api_key = get_api_key()
    data = get_weather_results(c_name, api_key)
    temp = "{0:.2f}".format(data["main"]["temp"])
    weather = data['weather'][0]['description']
    icon = data['weather'][0]['icon']
    location = data['name']
    country = data["sys"]["country"]
    longitude = "{0:.2f}".format(data["coord"]["lon"])
    latitude = "{0:.2f}".format(data["coord"]["lat"])
    return render_template('results.html',location=location, temp=temp, weather=weather, country=country, longitude=longitude, latitude=latitude,icon=icon)


@app.route('/windspeed', methods=['POST'])
def render_windspeed():
    api_key = get_api_key()
    data = get_weather_results(c_name, api_key)
    wind=data["wind"]["speed"]
    location = data['name']
    return render_template('windspeed.html',wind=wind,location=location)


@app.route('/pressure', methods=['POST'])
def render_pressure():
    api_key = get_api_key()
    data = get_weather_results(c_name, api_key)
    location = data['name']
    pressure = "{0:.2f}".format(data["main"]["pressure"])
    return render_template('pressure.html',pressure=pressure,location=location)


@app.route('/humidity', methods = ['POST'])
def render_humidity():
    api_key = get_api_key()
    data = get_weather_results(c_name, api_key)
    humidity = "{0:.2f}".format(data["main"]["humidity"])
    location = data['name']
    return render_template('humidity.html', humidity=humidity,location=location)


@app.route('/sunrise', methods=['POST'])
def render_sunrise():
    api_key = get_api_key()
    data = get_weather_results(c_name, api_key)
    sunrise = datetime.datetime.fromtimestamp(data["sys"]["sunrise"])
    location = data['name']
    return render_template('sunrise.html', sunrise=sunrise,location=location)


@app.route('/sunset', methods=['POST'])
def render_sunset():
    api_key = get_api_key()
    data = get_weather_results(c_name, api_key)
    sunset = datetime.datetime.fromtimestamp(data["sys"]["sunset"])
    location = data['name']
    return render_template('sunset.html', sunset=sunset,location=location)


def get_api_key():
    config = configparser.ConfigParser()
    config.read('config.ini')
    return config['openweathermap']['api']


def get_weather_results(c_name, api_key):
    api_url = "https://api.openweathermap.org/data/2.5/weather?q={}&appid={}&units=metric".format(c_name, api_key)
    r = requests.get(api_url)
    return r.json()


if __name__ == '__main__':
    app.run(debug=True)