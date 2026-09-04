"""A standalone script for downscaling and pulling bitmaps from images.

Decided to make this a standalone script. I'll probably just include the final bitmap data in the final project. My
hope is to be able to reuse this in the future, similar to the basic font set and drawing class I'm using.

TODO:
    *...Kinda surprised that works...Not sure what to do next actually. I guess I need to reduce blur on the resulting
        image.
    * Decide on final resolution. 100x100(50 lines) is current front runner.
    * Test new centering logic in alternate environments....I think it works...
    * Consider implementing linear interpolation for fade effects. I learned enough to do it, not sure if I'll have time
    * Look more into overwriting the terminal and manually flushing buffer to avoid overhead/flicker of clearing it.
"""
from pprint import pp, pprint

import sys, shutil
from PIL import Image


TERMINAL_WIDTH, _ = shutil.get_terminal_size()
PIXEL = '\u2584'
TARGET_HEIGHT = 100
TARGET_WIDTH = 100

img = Image.open(r'C:\Users\kazac\Downloads\Panera-Bread-Logo-cropped-squared.png')
img  = img.convert('RGB')
width, height = img.size

print(width)
print(height)

downscaled_img = img.resize((TARGET_WIDTH, TARGET_HEIGHT), Image.Resampling.LANCZOS)

print(f'{downscaled_img.width}, {downscaled_img.height}')
pixel_matrix = []
for y_coord in range(TARGET_HEIGHT):
    row_of_pixels = []
    for x_coord in range(TARGET_WIDTH):
        r, g, b = downscaled_img.getpixel((x_coord,y_coord))
        row_of_pixels.append((r, g, b))
    pixel_matrix.append(row_of_pixels)

print(len(pixel_matrix[0]))


def paint(bit_map):
    pad_length = (TERMINAL_WIDTH - TARGET_WIDTH) // 2
    padding = ' ' * pad_length
    print(len(padding))
    for y in range(0, TARGET_HEIGHT, 2):
        line = [padding]
        for x in range(TARGET_WIDTH):
            top = bit_map[y][x]
            bottom = bit_map[y + 1][x]

            tr, tg, tb = top
            br, bg, bb = bottom

            ansi_background = f'\x1b[48;2;{tr};{tg};{tb}m'
            ansi_foreground = f'\x1b[38;2;{br};{bg};{bb}m'

            line.append(f'{ansi_background}{ansi_foreground}{PIXEL}')

        sys.stdout.write(''.join(line) + '\x1b[0m\n')

paint(pixel_matrix)