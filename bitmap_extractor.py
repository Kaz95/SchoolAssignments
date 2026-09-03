"""A standalone script for downscaling and pulling bitmaps from images.

Decided to make this a standalone script. I'll probably just include the final bitmap data in the final project. My
hope is to be able to reuse this in the future, similar to the basic font set and drawing class I'm using.
"""

from PIL import Image

TERMINAL_WIDTH = 80

img = Image.open(r"C:\Users\kazac\Downloads\Panera-Bread-Logo.png")
img  = img.convert("RGB")
width, height = img.size

print(width)
print(height)

aspect_ratio = width / height
target_height = TERMINAL_WIDTH * aspect_ratio
print(aspect_ratio)
print(target_height)

# pixel_matrix = []
# for y in range(height):
#     row_of_pixels = []
#     for x in range(width):
#         r, g, b = img.getpixel((x,y))
#         print(r, g, b)