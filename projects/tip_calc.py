"""A tip calculator program.

TODO:
    * Had to use threading to prevent audio block. Built-in sound async wouldn't work with in-memory bytes.
        Need to clean up solution. Figure out exactly what the API is going to look like and implement.
    * Review and refactor.




"""
from __future__ import annotations

import io
import json
import sys
import threading
import time
import urllib.request
import wave
import winsound

TERMINAL_WIDTH = 80
"""Hardcoded terminal width in characters."""

CHARACTER_SPRITES = {'T': [0xE, 0x4, 0x4, 0x4, 0x4],
                     't': [0x4, 0xE, 0x4, 0x4, 0x4],
                     'h': [0xA, 0xA, 0xE, 0xA, 0xA],
                     'E': [0xE, 0x8, 0xE, 0x8, 0xE],
                     'N': [0xE, 0xA, 0xA, 0xA, 0xA],
                     'D': [0xC, 0xA, 0xA, 0xA, 0xC],
                     ' ': [0x0, 0x0, 0x0, 0x0, 0x0],
                     'i': [0x4, 0x4, 0x4, 0x4, 0x4],
                     'r': [0xE, 0xA, 0x8, 0x8, 0x8],
                     'o': [0xE, 0xA, 0xA, 0xA, 0xE],
                     '.': [0x0, 0x0, 0x0, 0x0, 0x4],
                     'P': [0xE, 0xA, 0xE, 0x8, 0x8],
                     'y': [0xA, 0xA, 0xE, 0x4, 0x4],
                     'A': [0x4, 0xA, 0xE, 0xA, 0xA],
                     'B': [0xC, 0xA, 0xC, 0xA, 0xC],
                     'R': [0xC, 0xA, 0xC, 0xA, 0xA],
                     '0': [0x0, 0xE, 0xA, 0xA, 0xA, 0xE, 0x0],
                     '1': [0x0, 0x4, 0x4, 0x4, 0x4, 0x4, 0x0],
                     '2': [0x0, 0xE, 0x2, 0xE, 0x8, 0xE, 0x0],
                     '3': [0x0, 0xE, 0x2, 0xE, 0x2, 0xE, 0x0],
                     '4': [0x0, 0xA, 0xA, 0xE, 0x2, 0x2, 0x0],
                     '5': [0x0, 0xE, 0x8, 0xE, 0x2, 0xE, 0x0],
                     '6': [0x0, 0xE, 0x8, 0xE, 0xA, 0xE, 0x0],
                     '7': [0x0, 0xE, 0x2, 0x2, 0x2, 0x2, 0x0],
                     '8': [0x0, 0xE, 0xA, 0xE, 0xA, 0xE, 0x0],
                     '9': [0x0, 0xE, 0xA, 0xE, 0x2, 0xE, 0x0],
                     '$': [0x4, 0xE, 0x8, 0xE, 0x2, 0xE, 0x4]
                     }
"""Sprite data represented in hexadecimal nibbles."""


class Drawing:
    """Class that handles all drawing logic."""
    top_left = "\u250c"  # ┌
    top_right = "\u2510"  # ┐
    bottom_left = "\u2514"  # └
    bottom_right = "\u2518"  # ┘
    horiz = "\u2500"  # ─
    vert = "\u2502"  # │
    circle = '\u2B24'  # ⬤
    upper_block = '\u2580'  # ▀
    lower_block = '\u2584'  # ▄
    full_block = '\u2588'  # █
    WHITE = "\033[97m"
    PANERA_GREEN = "\x1b[38;2;96;113;0m"
    PANERA_TAN = "\x1b[38;2;255;214;124m"
    RESET = "\033[0m"
    CURSOR_TO_TOP = "\x1b[H"
    CLEAR_SCREEN = "\x1b[2J"
    HIDE_CURSOR = "\x1b[?25l"
    SHOW_CURSOR = "\x1b[?25h"

    @staticmethod
    def get_pixel(row: int, x: int) -> int:
        """Retrieve a given 'pixel' at index x from 4 bit number.

        The pixel is represented by either a 1 or a 0. I'm shifting the bits until the one I'm interested in is the
        least significant bit. Then, I use an & mask of 1 to see if that bit is turned on or off.
        """
        return (row >> (3 - x)) & 1

    @classmethod
    def draw_word(cls, word: str, pad: str = '') -> None:
        """Draw a character sprite using Unicode block characters."""
        sprites = [CHARACTER_SPRITES[c] + [0] for c in word]
        for y in range(0, len(sprites[0]), 2):
            line = [pad]
            for sprite in sprites:
                for x in range(4):

                    top = cls.get_pixel(sprite[y], x)
                    bottom = cls.get_pixel(sprite[y + 1], x)

                    if top and bottom:
                        line.append(cls.WHITE + cls.full_block)

                    elif top:
                        line.append(cls.WHITE + cls.upper_block)


                    elif bottom:
                        line.append(cls.WHITE + cls.lower_block)

                    else:
                        line.append(' ')

            sys.stdout.write(''.join(line))
            print(cls.RESET)

    @classmethod
    def draw_window(cls, bill: str | int = 0, tip: str | int = 0) -> str:
        """Draw full calculator UI, including dynamic values."""
        print(cls.PANERA_TAN, end='')
        print(cls.CLEAR_SCREEN)
        print(cls.CURSOR_TO_TOP)

        bill = float(bill)
        tip = float(tip)

        print(cls.top_left + cls.horiz * 78 + cls.top_right)
        print('Welcome to:'.center(80))
        print()
        Drawing.draw_word('PANERA BREAD', pad=' ' * 18)
        print(cls.PANERA_TAN, end='')
        print(cls.vert + cls.horiz * 78 + cls.vert)
        for _ in range(15):

            if _ == 0:
                print(cls.vert + 'Gratuities'.center(38) + cls.vert + 'Bill'.center(39) + cls.vert)

            elif _ == 1:
                print(cls.vert + cls.horiz * 78 + cls.vert)

            elif _ == 3:
                print(cls.vert + f'A.) 15%:  ${bill * .15:04.2f}'.center(38) + cls.vert + f'Base: ${bill:04.2f}'.center(
                    39) + cls.vert)

            elif _ == 5:
                print(cls.vert + cls.horiz * 38 + cls.vert + cls.horiz * 39 + cls.vert)

            elif _ == 7:
                print(cls.vert + f'B.) 20%:  ${bill * .2:04.2f}'.center(38) + cls.vert + f'Tip: ${tip:04.2f}'.center(
                    39) + cls.vert)

            elif _ == 9:
                print(cls.vert + cls.horiz * 38 + cls.vert + cls.horiz * 39 + cls.vert)

            elif _ == 11:
                print(cls.vert + f'C.) 25%:  ${bill * .25:04.2f}'.center(
                    38) + cls.vert + f'Total: ${bill + tip:04.2f}'.center(39) + cls.vert)
            elif _ == 13:
                print(cls.vert + cls.horiz * 78 + cls.vert)

            elif _ == 14:
                if not bill:
                    print(cls.vert + 'Enter Bill: $$ or $$.$$'.center(78) + cls.vert)
                elif not tip:
                    print(cls.vert + 'Enter Tip: $$ or $$.$$'.center(78) + cls.vert)
                else:
                    print(cls.vert + '[R]eset, [T]ip, [E]xit...'.center(78) + cls.vert)
            else:
                print(cls.vert + cls.vert.center(78) + cls.vert)

        print(cls.bottom_left + cls.horiz * 78 + cls.bottom_right)

        uinput = input('? ')
        print(cls.RESET)
        return uinput



class TipCalc:
    """Core business logic. Gather user input based on context and draw UI."""
    BILL = 0
    TIP = 0
    OPTION = None
    EXIT = False

    TIP_OPTIONS = {'a': .15,
                   'b': .2,
                   'c': .25}
    AUDIO = None

    @classmethod
    def get_bill(cls) -> None:
        user_input = Drawing.draw_window()
        try:
            float(user_input)
            cls.BILL = user_input
        except ValueError:
            pass

    @classmethod
    def get_tip(cls) -> None:
        user_input = Drawing.draw_window(bill=cls.BILL)
        if user_input.lower() in cls.TIP_OPTIONS.keys():
            cls.TIP = float(cls.BILL) * cls.TIP_OPTIONS[user_input]
        else:
            try:
                float(user_input)
                cls.TIP = user_input
            except ValueError:
                pass

    @classmethod
    def get_option(cls) -> None:
        cls.OPTION = Drawing.draw_window(bill=cls.BILL, tip=cls.TIP)

        if cls.OPTION.lower() == 'r':
            cls.BILL = 0
            cls.TIP = 0
            play(cls.AUDIO)

        elif cls.OPTION.lower() == 't':
            cls.TIP = 0

        elif cls.OPTION.lower() == 'e':
            cls.EXIT = True

    @classmethod
    def to_float(cls, value) -> str:
        return f'{int(value):04.2f}'


# From other modules. I'd normally import, but limited to single file.
PANERA_LOGO_BITMAP_REMOTE = ('https://raw.githubusercontent.com/Kaz95/stdlib-only-toolkit/refs/heads/master/assets'
                             '/generated/panera_logo_bitmap.json')
TERMINAL_BLACK = (12, 12, 12)
CHANNELS = 2
SAMPLE_WIDTH = 2
SAMPLE_RATE = 44100

# # ANSI escapes
# RESET = "\x1b[0m"
# CURSOR_TO_TOP = "\x1b[H"  # Moves text cursor to 0,0 without clearing screen
# CLEAR_SCREEN = "\x1b[2J"  # Completely clears the terminal buffer once
# HIDE_CURSOR = "\x1b[?25l"  # Hides flashing text terminal bar
# SHOW_CURSOR = "\x1b[?25h"  # Restores terminal cursor state


def load_bitmap(remote_bitmap):
    with urllib.request.urlopen(remote_bitmap) as response:
        panera_logo_bitmap = json.load(response)
        return panera_logo_bitmap


def lerp(starting_color, target_color, progress):
    r = int(starting_color[0] + (target_color[0] - starting_color[0]) * progress)
    g = int(starting_color[1] + (target_color[1] - starting_color[1]) * progress)
    b = int(starting_color[2] + (target_color[2] - starting_color[2]) * progress)

    return r, g, b


def render_frame(bit_map, progress, terminal_width, is_black=True, pad=False):
    """Build one frame as a finished string, without writing anything."""
    height = len(bit_map)
    width = len(bit_map[0])
    if pad:
        pad_length = (terminal_width - width) // 2
        pad = ' ' * pad_length
    else:
        pad = ''

    frame_lines = [Drawing.CURSOR_TO_TOP]
    for y in range(0, height, 2):
        line_buffer = [pad]
        for x in range(width):
            original_top = bit_map[y][x]
            original_bottom = bit_map[y + 1][x]

            if is_black:
                top_rgb = lerp(TERMINAL_BLACK, original_top, progress)
                bot_rgb = lerp(TERMINAL_BLACK, original_bottom, progress)
            else:
                top_rgb = lerp(original_top, TERMINAL_BLACK, progress)
                bot_rgb = lerp(original_bottom, TERMINAL_BLACK, progress)

            bg_ansi = f"\x1b[48;2;{top_rgb[0]};{top_rgb[1]};{top_rgb[2]}m"
            fg_ansi = f"\x1b[38;2;{bot_rgb[0]};{bot_rgb[1]};{bot_rgb[2]}m"

            line_buffer.append(f"{bg_ansi}{fg_ansi}{Drawing.lower_block}")

        frame_lines.append("".join(line_buffer) + Drawing.RESET)

    return "\n".join(frame_lines) + "\n"


def precompute_interpolation_frames(bit_map, terminal_width, steps):
    """Render all frames of the animation in advance and store them in a list."""
    frames = []

    for step in range(steps + 1):
        progress = step / steps
        frames.append(render_frame(bit_map, progress, terminal_width, is_black=True))

    for step in range(steps + 1):
        progress = step / steps
        frames.append(render_frame(bit_map, progress, terminal_width, is_black=False))

    return frames


def play_animation_sequence(matrix, steps=60, sleep_rate=0.05):
    frames = precompute_interpolation_frames(matrix, TERMINAL_WIDTH, steps)
    fade_in_frame_count = steps + 1

    sys.stdout.write(Drawing.HIDE_CURSOR)
    sys.stdout.write(Drawing.CLEAR_SCREEN)

    for i, frame in enumerate(frames):
        sys.stdout.write(frame)
        sys.stdout.flush()

        if i == fade_in_frame_count:
            time.sleep(3)
        else:
            time.sleep(sleep_rate)

    sys.stdout.write(Drawing.SHOW_CURSOR)


def load_remote_raw_audio_bytes():
    with urllib.request.urlopen('https://raw.githubusercontent.com/Kaz95/stdlib-only-toolkit/refs/heads/master/assets'
                                '/generated/kaching_audio_bytes') as response:
        raw_audio_bytes = response.read()
        return raw_audio_bytes


def play_kaching(loaded_bytes):
    # How have I never used io library before now?!
    bytes_io = io.BytesIO()
    # Set header and load
    with wave.open(bytes_io, "wb") as wav_write:
        wav_write.setnchannels(CHANNELS)
        wav_write.setsampwidth(SAMPLE_WIDTH)
        wav_write.setframerate(SAMPLE_RATE)
        wav_write.writeframes(loaded_bytes)

    winsound.PlaySound(bytes_io.getvalue(), winsound.SND_MEMORY)


def play(audio_bytes):
    play_thread = threading.Thread(target=play_kaching, args=(audio_bytes,))
    play_thread.daemon = True  # Allows the program to exit even if the audio is still playing
    play_thread.start()


if __name__ == '__main__':
    raw_audio = load_remote_raw_audio_bytes()
    TipCalc.AUDIO = raw_audio
    logo_bitmap = load_bitmap(PANERA_LOGO_BITMAP_REMOTE)
    play_animation_sequence(logo_bitmap, 40, .05)

    while not TipCalc.EXIT:
        if not TipCalc.BILL:
            TipCalc.get_bill()

        elif not TipCalc.TIP:
            TipCalc.get_tip()

        else:
            TipCalc.get_option()
