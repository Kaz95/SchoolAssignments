"""A tip calculator program.

TODO:
    * Review and refactor.
    * Add docstrings
    * Add typehints.
    * Sanitize inputs.
    * Start integrating logo. Will have to copy in parts of extractor and paint since I can't do imports.
    * Allow tip option number to be used in place of a value.
    * Calc tax
    * Allow change in preset tip %?



"""
import sys
import bitmap_extractor
import paint

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
    RESET = "\033[0m"
    CURSOR_TO_TOP = "\x1b[H"
    CLEAR_SCREEN = "\x1b[2J"

    @staticmethod
    def get_pixel(row: int, x: int) -> int:
        """Retrieve a given 'pixel' at index x from 4 bit number.

        The pixel is represented by either a 1 or a 0.
        """
        return (row >> (3 - x)) & 1

    @classmethod
    def draw_word(cls, word, pad=''):
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
    def draw_window(cls, bill=0, tip=0):
        """Draw full calculator UI, including dynamic values."""
        print(cls.CLEAR_SCREEN)
        print(cls.CURSOR_TO_TOP)

        bill = float(bill)
        tip = float(tip)


        print(cls.top_left + cls.horiz * 78 + cls.top_right)
        subject = f'{EmojiUnicodes.computer} Subject {EmojiUnicodes.computer}'
        print(subject.center(80))
        print(cls.vert + cls.horiz * 78 + cls.vert)
        for _ in range(15):

            if _ == 0:
                print(cls.vert + 'Gratuities'.center(38) + cls.vert + 'Bill'.center(39) + cls.vert)

            elif _ == 1:
                print(cls.vert + cls.horiz * 78 + cls.vert)

            elif _ == 3:
                print(cls.vert + f'1.) 15%:  ${bill * .15:04.2f}'.center(38) + cls.vert + f'Base: ${bill:04.2f}'.center(39) + cls.vert)

            elif _ == 5:
                print(cls.vert + cls.horiz * 38 + cls.vert + cls.horiz * 39 + cls.vert)

            elif _ == 7:
                print(cls.vert + f'2.) 20%:  ${bill * .2:04.2f}'.center(38) + cls.vert + f'Tip: ${tip:04.2f}'.center(39) + cls.vert)

            elif _ == 9:
                print(cls.vert + cls.horiz * 38 + cls.vert + cls.horiz * 39 + cls.vert)

            elif _ == 11:
                print(cls.vert + f'3.) 25%:  ${bill * .25:04.2f}'.center(38) + cls.vert + f'Total: ${bill + tip:04.2f}'.center(39) + cls.vert)
            elif _ == 13:
                print(cls.vert + cls.horiz * 78 + cls.vert)

            elif _ == 14:
                if not bill:
                    print(cls.vert + 'Enter Bill:'.center(78) + cls.vert)
                elif not tip:
                    print(cls.vert + 'Enter Tip:'.center(78) + cls.vert)
                else:
                    print(cls.vert + '[R]eset, [T]ip, [E]xit...'.center(78) + cls.vert)
            else:
                print(cls.vert + cls.vert.center(78) + cls.vert)
        print(cls.bottom_left + cls.horiz * 78 + cls.bottom_right)
        uinput = input('? ')
        return uinput


class ColorEscapeSequences:
    """Enumerated ANSI escape sequences.

    I wasn't sure if I wanted to use the actual enum module or not. This type of data is a perfect fit for an enum, but
    there is no reason to maintain uniqueness and immutability for this small project. I decided an enum would only
    make access more verbose, with none of the normal benefits.
    """

    RESET = "\033[0m"
    WHITE = "\033[37m"  # White
    GREEN = "\033[32m"  # Green
    PHOSPHORGREEN = "\033[1;92m"  # Bold, High-Intensity green.


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

    def __getattribute__(self, name: str, /):
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
    BILL = 0
    TIP = 0
    OPTION = None
    EXIT = False

    @classmethod
    def get_bill(cls):
        cls.BILL = Drawing.draw_window()

    @classmethod
    def get_tip(cls):
        cls.TIP = Drawing.draw_window(bill=cls.BILL)

    @classmethod
    def get_option(cls):
        cls.OPTION = Drawing.draw_window(bill=cls.BILL, tip=cls.TIP)

        if cls.OPTION.lower() == 'r':
            cls.BILL = 0
            cls.TIP = 0

        elif cls.OPTION.lower() == 't':
            cls.TIP = 0

        elif cls.OPTION.lower() == 'e':
            cls.EXIT = True



    @classmethod
    def to_float(cls, value):
        return f'{int(value):04.2f}'

if __name__ == '__main__':
    logo_bitmap = bitmap_extractor.load_bitmap(bitmap_extractor.panera_logo_bitmap_remote)
    paint.play_animation_sequence(logo_bitmap, 60, .05)
    TipCalc.get_bill()
    TipCalc.get_tip()
    TipCalc.get_option()
    while not TipCalc.EXIT:
        if not TipCalc.BILL:
            TipCalc.get_bill()

        elif not TipCalc.TIP:
            TipCalc.get_tip()

        else:
            TipCalc.get_option()

        # if TipCalc.OPTION:
        #     if TipCalc.OPTION.lower() == 'r':
        #         TipCalc.BILL = 0
        #         TipCalc.TIP = 0
        #         TipCalc.
        #
        # elif TipCalc.OPTION.lower() == 't':
        #     pass
        # elif TipCalc.OPTION.lower() == 'e':
        #     pass
        # else:
        # print('Invalid option.')
    # _bill = Drawing.draw_window()
    # _bill = f'{int(_bill):04.2f}'
    # _tip = Drawing.draw_window(_bill)
    # _tip = f'{int(_tip):04.2f}'
    # _option = Drawing.draw_window(_bill, _tip)


    # Drawing.draw_word('$123')