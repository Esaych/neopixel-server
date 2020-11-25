# Simple test for NeoPixels on Raspberry Pi
import time
import board
import neopixel
import importlib
import sys

NUM_PIXELS = 36
PIN = board.D18
ORDER = neopixel.GRB
PIXELS = neopixel.NeoPixel(PIN, NUM_PIXELS, brightness=0.5, auto_write=False, pixel_order=ORDER)

COLORS = [[0,0,0]] * 3
OLD_COLORS = COLORS

def show_rgb(red, green, blue):
    PIXELS.fill((red, green, blue))
    PIXELS.show()

def show_color(color):
    for board in range(1,4):
        show_rgb3(board, color[board-1][0], color[board-1][1], color[board-1][2])
    
    #print(PIXELS)
    PIXELS.show()

def show_rgb3(boardNum, red, green, blue):
    for i in range((boardNum-1)*12, (boardNum)*12):
        #sys.stderr.write(str(i+1))
        PIXELS[i] = (red, green, blue)

def get_step_color(colora, colorb, step, total):
    red_delta = (colorb[0] - colora[0]) * step / total
    green_delta = (colorb[1] - colora[1]) * step / total
    blue_delta = (colorb[2] - colora[2]) * step / total
    #sys.stderr.write("Deltas: {} {} {} {}".format(red_delta, green_delta, blue_delta, step))

    new_color = [x + y for x, y in zip(colora, [int(red_delta), int(green_delta), int(blue_delta)])]

    return new_color

def gradual_color(new_color, ms_wait=10, seconds=5):
    global OLD_COLORS
    global COLORS

    OLD_COLORS = COLORS
    COLORS = new_color

    #sys.stderr.write(str(OLD_COLORS))
    #sys.stderr.write(str(COLORS))

    step_count = seconds * 1000 / ms_wait

    for step in range(0, int(step_count)):
        color1 = get_step_color(OLD_COLORS[0], COLORS[0], step, step_count)
        color2 = get_step_color(OLD_COLORS[1], COLORS[1], step, step_count)
        color3 = get_step_color(OLD_COLORS[2], COLORS[2], step, step_count)

        new_color = [color1, color2, color3]
        #sys.stderr.write(str(new_color))

        show_color(new_color)

        time.sleep(0.001*ms_wait)


def gradual_rgb(red, green, blue, red2, green2, blue2, red3, green3, blue3, seconds=5):
    color = [[red, green, blue], [red2, green2, blue2], [red3, green3, blue3]]
    gradual_color(color)

if __name__ == "__main__":
    import sys
    show_rgb(int(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]))
