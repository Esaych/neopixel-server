import sys
import array
import control
import time
import neopixel
import board
import matplotlib.cm
import select
import os

num_pixels = 36
pixel_pin = board.D18
ORDER = neopixel.GRB
FIFO_PATH = '/tmp/cava'

def get_spaced_colors(n):
    max_value = 16581375
    interval = int(max_value / n)
    #print(interval)
    colors = [hex(i)[2:].zfill(6) for i in range(0, max_value, interval)]
    #print(colors)

    return [(int(color[:2], 16),
             int(color[2:4], 16),
             int(color[4:6], 16)) for color in colors]

def do_cmap(cmap, num):
    if num == 0: return (0, 0, 0)

    r, g, b, _ = cmap(num / 255)
    return (int(r*255),int(g*255),int(b*255))

def read_data(eq, cmap):
    #print("eq: " + eq)
    nums = eq.split(';')
    if (len(nums) != 4):
        return
    nums.pop()
    # led_colors = list(map(lambda num: colors[num], nums))
    led_colors = list(map(lambda num: do_cmap(cmap, int(num)), nums))
    control.show_color(led_colors)

def flush_pipe(fifo):
    time_mark = time.time()
    delta = 0
    while True:
        if delta > 0.015:
            return
        else:
            fifo.readline()
            delta = time.time() - time_mark
            time_mark = time.time()

def handle_fifo():
    cmap = matplotlib.cm.get_cmap("inferno")

    try:
        os.mkfifo(FIFO_PATH)
    except FileExistsError:
        pass
    except OSError as oe:
        raise

    #read from pipe
    with open(FIFO_PATH) as fifo:
        buff = ''
        while True:
            flush_pipe(fifo)
            # select.select([fifo],[],[fifo])
            chunk = fifo.readline()
            read_data(chunk, cmap)                    

if __name__ == '__main__':
    handle_fifo()
