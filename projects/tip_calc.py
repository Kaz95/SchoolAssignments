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

PANERA_LOGO_BITMAP_REMOTE = 'https://raw.githubusercontent.com/Kaz95/SchoolAssignments/refs/heads/master/panera_logo_bitmap.json'
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


# First time actually finding a solid use case for a MetaClass!
class PadZeroMeta(type):
    """EmojiUnicodes Metaclass."""

    # Trying to add this to class or references just about any way other than class level static method causes recursion
    # I mostly understand why, but I need to look into it more. TODO: Fully understand class lookup.
    @staticmethod
    def fill_emoji_unicode(emoji: str) -> str:
        """Pad emoji strings with correct amount of '0's."""
        split_emoji = emoji.split(r'\u')
        padded_code = rf'\U{split_emoji[0]:0>8}'

        if len(split_emoji) > 1:
            padded_code = padded_code + rf'\u{split_emoji[1]}'

        # Learned some cool stuff about run-time vs compilation.
        # Need to manually decode. Dynamic string isn't available at compile time, and isn't recognized as an ANSI escape.
        emoji = padded_code.encode('utf-8').decode('unicode_escape')
        return emoji

    def __getattribute__(self, name: str):
        value = super().__getattribute__(name)

        # Block dunder methods.
        if name.startswith('__') and name.endswith('__'):
            return value
        else:
            new_val = PadZeroMeta.fill_emoji_unicode(value)
            return new_val


class EmojiUnicodes(metaclass=PadZeroMeta):
    """Emoji Unicode string constants."""
    blood = '1FA78'
    clock = r'1F570\uFE0F'
    programmer = '1F4BE'
    computer = r'1F5A5\uFE0F'
    fish = '1F3A3'
    baseball = '26BE'
    joystick = r'1F579\uFE0F'
    planet = '1F30C'
    robot = '1F916'
    book = '1F4D6'
    thanks = '1F64F'
    alien = '1F47D'
    bread = '1F35E'
    flat_bread = '1FAD3'


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
TERMINAL_BLACK = (12, 12, 12)
CHANNELS = 2
SAMPLE_WIDTH = 2
SAMPLE_RATE = 44100


def load_bitmap(remote_bitmap):
    with urllib.request.urlopen(remote_bitmap) as response:
        panera_logo_bitmap = json.load(response)
        return panera_logo_bitmap


def lerp(starting_color, target_color, progress):
    r = int(starting_color[0] + (target_color[0] - starting_color[0]) * progress)
    g = int(starting_color[1] + (target_color[1] - starting_color[1]) * progress)
    b = int(starting_color[2] + (target_color[2] - starting_color[2]) * progress)

    return r, g, b


def paint_a_frame(bit_map, progress, terminal_width, is_black=True, pad=False):
    """This function is super inefficient. I realized this as a result of trying to run it in online environments.

    There is a massive amount of data being pushed. I think online tools are I/O bottle knecked on the networking
    side of things. I also believe most online editors are running inside a docker container at this point, and only
    allocated a very small amount of resources. I wouldn't be surprised if the containers are also throttled depending on
    work load. I could attempt to make it more efficient(the nested loop is O(n^2) I think), but the real solution
    is to run it locally. If I were trying to get it to run online, I'd start by only sending a new ANSI color code
    when a pixel has a different color from the previous. I think this would significantly reduce the overall payload.
    I should probably also append the reset and newline escapes to the line buffer list to avoid string concatenation
    all together. Appending to end of a list is O(1) constant time, while creating a new string in a loop is O(n^2)
    at its worst.
    """
    # Overwrite the previous frame by pinning cursor back to the top left corner
    sys.stdout.write(Drawing.CURSOR_TO_TOP)

    height = len(bit_map)
    width = len(bit_map[0])
    if pad:
        pad_length = (terminal_width - width) // 2
        pad = ' ' * pad_length
    else:
        pad = ''
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

        sys.stdout.write("".join(line_buffer) + Drawing.RESET + "\n")
    sys.stdout.flush()


def play_animation_sequence(matrix, steps=60, sleep_rate=0.05):
    # Hide interface cursors
    sys.stdout.write(Drawing.HIDE_CURSOR)
    sys.stdout.write(Drawing.CLEAR_SCREEN)

    for step in range(steps + 1):
        progress = step / steps
        paint_a_frame(matrix, progress, TERMINAL_WIDTH)
        time.sleep(sleep_rate)

    for step in range(steps + 1):
        progress = step / steps
        paint_a_frame(matrix, progress, TERMINAL_WIDTH, is_black=False)
        if step == 0:
            time.sleep(3)
        else:
            time.sleep(sleep_rate)

    sys.stdout.write(Drawing.SHOW_CURSOR)


def load_remote_raw_audio_bytes():
    with urllib.request.urlopen(
            'https://github.com/Kaz95/SchoolAssignments/raw/refs/heads/master/raw_audio_bytes') as response:
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
    play_animation_sequence(logo_bitmap, 60, .05)

    while not TipCalc.EXIT:
        if not TipCalc.BILL:
            TipCalc.get_bill()

        elif not TipCalc.TIP:
            TipCalc.get_tip()

        else:
            TipCalc.get_option()
