"""Border/box drawing, ANSI color and cursor-control constants, and the bitmap-font glyph rendering."""
import sys

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
    def draw_window(cls) -> str:
        """Draw full calculator UI, including dynamic values."""
        print(cls.CLEAR_SCREEN)
        print(cls.CURSOR_TO_TOP)


        print(cls.top_left + cls.horiz * 78 + cls.top_right)
        print('Title'.center(80))
        print(cls.vert + cls.horiz * 78 + cls.vert)
        for _ in range(15):

            if _ == 0:
                print(cls.vert +  'Headers'.center(78) + cls.vert)

            elif _ == 1:
                print(cls.vert + cls.horiz * 78 + cls.vert)

            else:
                print(cls.vert + ' ' * 78 + cls.vert)

        print(cls.bottom_left + cls.horiz * 78 + cls.bottom_right)

        uinput = input('? ')
        print(cls.RESET)
        return uinput

if __name__ == '__main__':
    Drawing.draw_window()