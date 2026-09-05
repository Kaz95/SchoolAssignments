"""A standalone script for painting bitmaps in the terminal.

Just about finished planning and realized this is probably best kept as a standalone script similar to extractor.
I'm going to want to reuse this for future projects, but I'm not sure how I will go about including it.
"""
import shutil
import sys
import time

TERMINAL_WIDTH, _ = shutil.get_terminal_size()

TERMINAL_BLACK = (12, 12, 12)
PIXEL = '\u2584'

# ANSI escapes
RESET = "\x1b[0m"
CURSOR_TO_TOP = "\x1b[H"  # Moves text cursor to 0,0 without clearing screen
CLEAR_SCREEN = "\x1b[2J"  # Completely clears the terminal buffer once
HIDE_CURSOR = "\x1b[?25l"  # Hides flashing text terminal bar
SHOW_CURSOR = "\x1b[?25h"  # Restores terminal cursor state

def lerp(starting_color, target_color, progress):
    r = int(starting_color[0] + (target_color[0] - starting_color[0]) * progress)
    g = int(starting_color[1] + (target_color[1] - starting_color[1]) * progress)
    b = int(starting_color[2] + (target_color[2] - starting_color[2]) * progress)

    return r, g, b

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


def paint_a_frame(bit_map, progress, terminal_width):

    # Overwrite the previous frame by pinning cursor back to the top left corner
    sys.stdout.write(CURSOR_TO_TOP)

    height = len(bit_map)
    width = len(bit_map[0])
    pad_length = (terminal_width - width) // 2
    padding = ' ' * pad_length
    for y in range(0, height, 2):
        line_buffer = [padding]
        for x in range(width):
            original_top = bit_map[y][x]
            original_bottom = bit_map[y + 1][x]

            top_rgb = lerp(original_top, TERMINAL_BLACK, progress)
            bot_rgb = lerp(original_bottom, TERMINAL_BLACK, progress)

            bg_ansi = f"\x1b[48;2;{top_rgb[0]};{top_rgb[1]};{top_rgb[2]}m"
            fg_ansi = f"\x1b[38;2;{bot_rgb[0]};{bot_rgb[1]};{bot_rgb[2]}m"

            line_buffer.append(f"{bg_ansi}{fg_ansi}{PIXEL}")

        sys.stdout.write("".join(line_buffer) + RESET + "\n")
    sys.stdout.flush()


def play_animation_sequence(matrix, steps=60, sleep_rate=0.05):
    # Hide interface cursors
    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.write(CLEAR_SCREEN)

    for step in range(steps + 1):
        progress = step / steps
        paint_a_frame(matrix, progress, TERMINAL_WIDTH)
        if step == 0:
            time.sleep(3)
        else:
            time.sleep(sleep_rate)

    sys.stdout.write(SHOW_CURSOR)
    print("\nAnimation Complete.")