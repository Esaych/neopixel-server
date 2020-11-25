from flask import Flask
from threading import Thread
import queue
import control, weather, logging

app = Flask(__name__)
run_weather = False
weather_thread = None

@app.route('/rgb/<red>/<green>/<blue>')
def rgb(red, green, blue):
    red = int(red)
    green = int(green)
    blue = int(blue)

    control.show_rgb(red, green, blue)
    
    return "Changed to R: {} G: {} B: {}".format(red, green, blue)

@app.route('/rgb3/<red>/<green>/<blue>/<red2>/<green2>/<blue2>/<red3>/<green3>/<blue3>')
def rgb3(red, green, blue, red2, green2, blue2, red3, green3, blue3):
    control.show_color([[int(red), int(green), int(blue)], 
            [int(red2), int(green2), int(blue2)], 
            [int(red3), int(green3), int(blue3)]])

    return "Changed to R{}G{}B{} R{}G{}B{} R{}G{}B{}".format(red, green, blue, red2, green2, blue2, red3, green3, blue3)

@app.route('/fade/<red>/<green>/<blue>/<red2>/<green2>/<blue2>/<red3>/<green3>/<blue3>')
def fade(red, green, blue, red2, green2, blue2, red3, green3, blue3):
    control.gradual_rgb(int(red), int(green), int(blue),
            int(red2), int(green2), int(blue2),
            int(red3), int(green3), int(blue3))

    return "Faded to R{}G{}B{} R{}G{}B{} R{}G{}B{}".format(red, green, blue, red2, green2, blue2, red3, green3, blue3)

@app.route('/weather')
def weather():
    global run_weather
    global weather_thread
    run_weather = True
    weather_thread = Thread(target = weather_service, args=("Weather Service",))
    weather_thread.start()
    return "Started the weather sequence"

def weather_service(thread_name):
    import weather
    import time
    logging.info("Thread %s: starting", thread_name)
    global run_weather
    while run_weather:
        weather.set_weather()
        seconds = 0
        while run_weather and seconds < 30:
            time.sleep(1)
            seconds+=1
        
        weather.set_temps()
        seconds = 0
        while run_weather and seconds < 30:
            time.sleep(1)
            seconds+=1

@app.route('/stop_weather')
def stop_weather():
    global run_weather
    run_weather = False
    weather_thread.join()
    control.show_color([[0,0,0],[0,0,0],[0,0,0]])
    return "Stopped weather sequence"
