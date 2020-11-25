import control
import config

import requests, json, time

cache_weather = {}
cache_time = 0

api_key = config.weather["api_key"]

def collect_weather():
    global cache_weather
    global cache_time

    if cache_time > time.time() - 600:
        return cache_weather
    else:
        print("querying for new weather")
        try:
            seattle = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Seattle&appid="+api_key).json()
            maryland = requests.get("http://api.openweathermap.org/data/2.5/weather?q=North%20Potomac&appid="+api_key).json()
            phoenix = requests.get("http://api.openweathermap.org/data/2.5/weather?q=Phoenix&appid="+api_key).json()
            cache_weather = [phoenix, maryland, seattle] #[BOTTOM MIDDLE TOP]
            cache_time = time.time()
            print(str(cache_weather))
        except:
            print("Network failure retreiving weather")
        return cache_weather

def translate_temp_to_color(temp):
    #90F 305K - RED (255,0,0)
    #70F 294K - YELLOW (255,255,0)
    #55F 286K - WHITE (255,255,255)
    #40F 278K - CYAN (0,255,255)
    #25F 269K - BLUE (0,0,255)

    red = (temp - 278) / (286 - 278) * 255
    green = (temp - 269) / (278 - 269) * 255
    if temp > 286:
        green = 255 - (temp - 294) / (305 - 294) * 255
    blue = 255 - (temp - 286) / (294 - 286) * 255

    red = keepRGB(red)
    green = keepRGB(green)
    blue = keepRGB(blue)

    return [red, green, blue]

desc_color = {
        '01d': [255,255,40],
        '02d': [255,255,40],
        '03d': [128,155,155],
        '04d': [0,115,113],
        '09d': [40,50,255],
        '10d': [0,10,224],
        '11d': [255,251,0],
        '13d': [255,255,255],
        '50d': [165,58,0],
        '01n': [255,255,40],
        '02n': [255,255,40],
        '03n': [128,155,155],
        '04n': [0,115,113],
        '09n': [40,50,255],
        '10n': [0,10,224],
        '11n': [255,251,0],
        '13n': [255,255,255],
        '50n': [165,58,0]
        }

def translate_description_to_color(desc):
    global desc_color
    
    if desc[1]['sunset'] < time.time() or desc[1]['sunrise'] > time.time():
        return [70,0,132]
    return desc_color[desc[0]]

def keepRGB(val):
    if val > 255:
        return 255
    if val < 0:
        return 0
    return int(val)
    
def set_temps():
    vals = collect_weather()
    #print(vals)

    temps = list(map(lambda x: x['main']['temp'], vals))
    #print(temps)

    colors = list(map(lambda temp: translate_temp_to_color(temp), temps))
    #print(colors)

    control.gradual_color(colors)

def set_weather():
    vals = collect_weather()
    #print(vals)

    desc = list(map(lambda x: [x['weather'][0]['icon'], x['sys']], vals))
    #print(desc)

    colors = list(map(lambda desc : translate_description_to_color(desc), desc))
    #print(colors)

    control.gradual_color(colors)

if __name__ == "__main__":
    while True:
        set_weather()
        time.sleep(60)
        set_temps()
        time.sleep(60) 

