from flask import Flask
from threading import Thread
import queue
import control, weather, logging
# import time
# from timeloop import Timeloop
# from datetime import timedelta

# tl = Timeloop()

app = Flask(__name__)
run_weather = False
weather_thread = None
run_music = False
music_thread = None

@app.route('/rgb/<red>/<green>/<blue>')
def rgb(red, green, blue):
    red = int(red)
    green = int(green)
    blue = int(blue)
    stop_services()

    control.show_rgb(red, green, blue)
    
    return "Changed to R: {} G: {} B: {}".format(red, green, blue)

@app.route('/rgb3/<red>/<green>/<blue>/<red2>/<green2>/<blue2>/<red3>/<green3>/<blue3>')
def rgb3(red, green, blue, red2, green2, blue2, red3, green3, blue3):
    control.show_color([[int(red), int(green), int(blue)], 
            [int(red2), int(green2), int(blue2)], 
            [int(red3), int(green3), int(blue3)]])

    stop_services()

    return "Changed to R{}G{}B{} R{}G{}B{} R{}G{}B{}".format(red, green, blue, red2, green2, blue2, red3, green3, blue3)

@app.route('/fade/<red>/<green>/<blue>/<red2>/<green2>/<blue2>/<red3>/<green3>/<blue3>')
def fade(red, green, blue, red2, green2, blue2, red3, green3, blue3):
    control.gradual_rgb(int(red), int(green), int(blue),
            int(red2), int(green2), int(blue2),
            int(red3), int(green3), int(blue3))

    stop_services()

    return "Faded to R{}G{}B{} R{}G{}B{} R{}G{}B{}".format(red, green, blue, red2, green2, blue2, red3, green3, blue3)

@app.route('/weather')
def weather():
    global run_weather
    global weather_thread

    if run_weather:
        return "Weather is already running"
    stop_services()

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
    global weather_thread

    try:
        run_weather = False
        weather_thread.join()
        control.show_color([[0,0,0],[0,0,0],[0,0,0]])
        return "Stopped weather sequence"
    except:
        return "Weather already stopped"

@app.route('/music')
def music():
    global run_music
    global music_thread

    if run_music:
        return "Music is already running"
    stop_services()

    run_music = True
    music_thread = Thread(target = music_service, args=("Music Service",))
    music_thread.start()
    return "Started the music listener"

def music_service(thread_name):
    import music
    print("Thread starting:", thread_name)
    global music_thread
    while run_music:
        music.mk_fifo()
        #read from pipe
        with open(music.FIFO_PATH) as fifo:
            music.flush_pipe(fifo)
            while run_music:
                vis_data = fifo.readline()
                # print(vis_data)
                music.read_data(vis_data) 

@app.route('/stop_music')
def stop_music():
    global run_music
    global music_thread

    try:
        run_music = False
        music_thread.join()
        control.show_color([[0,0,0],[0,0,0],[0,0,0]])
        return "Stopped music sequence"
    except:
        return "Music already stopped"

@app.route('/track_data/<trackid>')
def track_data(trackid):
    import music
    import time
    time.sleep(1)
    color = music.set_cmap(hash(trackid))
    return 'Changed color to %s' % color

def stop_services():
    print('stopping services')
    stop_weather()
    stop_music()
