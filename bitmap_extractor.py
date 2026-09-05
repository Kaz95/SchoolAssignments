"""A standalone script for downscaling and pulling bitmaps from images.

Decided to make this a standalone script. I'll probably just include the final bitmap data in the final project. My
hope is to be able to reuse this in the future, similar to the basic font set and drawing class I'm using.

TODO:
    *...Kinda surprised that works...Not sure what to do next actually. I guess I need to reduce blur on the resulting
        image.
    * Decide on final resolution. 100x100(50 lines) is current front runner.
    * Basic Linear Interpolated Fade effect implemented. Now I need to reverse it to fade in too.
    * Centering still working even with fade. A bit more testing and I'll actually trust it not to break.
"""
import shutil
from PIL import Image
from paint import play_animation_sequence, paint

TERMINAL_WIDTH, _ = shutil.get_terminal_size()

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




# paint(pixel_matrix, TERMINAL_WIDTH, TARGET_HEIGHT, TARGET_WIDTH)
play_animation_sequence(pixel_matrix, 60, 0.05)