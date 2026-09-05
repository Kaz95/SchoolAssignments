"""A standalone script for painting bitmaps in the terminal.

Just about finished planning and realized this is probably best kept as a standalone script similar to extractor.
I'm going to want to reuse this for future projects, but I'm not sure how I will go about including it.
"""
import sys

PIXEL = '\u2584'

def paint(bit_map, terminal_width,target_height, target_width):
    pad_length = (terminal_width - target_width) // 2
    padding = ' ' * pad_length
    print(len(padding))
    for y in range(0, target_height, 2):
        line = [padding]
        for x in range(target_width):
            top = bit_map[y][x]
            bottom = bit_map[y + 1][x]

            tr, tg, tb = top
            br, bg, bb = bottom

            ansi_background = f'\x1b[48;2;{tr};{tg};{tb}m'
            ansi_foreground = f'\x1b[38;2;{br};{bg};{bb}m'

            line.append(f'{ansi_background}{ansi_foreground}{PIXEL}')

        sys.stdout.write(''.join(line) + '\x1b[0m\n')