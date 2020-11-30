import os
import urllib.request

contents = urllib.request.urlopen("http://192.168.0.173:5000/track_data/"+os.environ['TRACK_ID']).read()

if os.environ['PLAYER_EVENT'] == "playing":
    urllib.request.urlopen("http://192.168.0.173:5000/music").read()
elif os.environ['PLAYER_EVENT'] == "paused":
    urllib.request.urlopen("http://192.168.0.173:5000/weather").read()
