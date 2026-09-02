"""A tip calculator program.

TODO:
    * Figure out how to draw the Panera Logo. Current thought is downscaling the image and then taking the bitmap.
        I also need to increase resolution. Look into other methods of drawing pixels discovered during last project.
        Such as using horizontal half blocks with foreground and background colors. If I can get the resolution high
        enough, I can draw the entire logo including the name in one pass. If not I can always do name the old way
        and have it appear after the logo.
    *
    * Solidify the UI of the tip calc. Nothing too similar to last project. Probably no use of time.sleep().
        Tip calc should be snappy.
    *
    * Calc tax


"""
import time

TERMINAL_WIDTH = 80

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
                     'R': [0xC, 0xA, 0xC, 0xA, 0xA]}

class Drawing:
    """Class that handles all drawing logic."""
    top_left = "\u250c"  # ┌
    top_right = "\u2510"  # ┐
    bottom_left = "\u2514"  # └
    bottom_right = "\u2518"  # ┘
    horiz = "\u2500"  # ─
    vert = "\u2502"  # │
    half_block = "\u2588"  # █
    circle = '\u2B24'  # ⬤

    @classmethod
    def print_character_sprite(cls, word: str) -> None:
        """Draw character sprite base on given sprite data."""

        # Need to double up to maintain square aspect ratio
        full_block = cls.half_block * 2
        double_space = "  "

        sprite_word = []
        for char in word:
            sprite_word.append(CHARACTER_SPRITES[char])

        for _ in range(5):
            row_string = ''
            for char in sprite_word:
                row = f'{char[_]:05b}'
                graphic_row = ''.join(full_block if char == "1" else double_space for char in row)
                row_string += graphic_row
            row_string = row_string.center(TERMINAL_WIDTH)
            Drawing.draw_ticker_row(row_string, emoji=True)

    @classmethod
    def draw_window(cls) -> None:
        # TODO: Will need completely rework this method. Should draw the tip calc.
        pass
        # """Draw a 'window' with boarder Unicode characters."""
        # ootext = False
        # print(cls.top_left + cls.horiz * 78 + cls.top_right)
        # for _ in range(22):
        #     if _ == 0:
        #         subject = f'{entry.emoji} {entry.subject} {entry.emoji}'
        #         print(subject.center(80))
        #         continue
        #     elif _ == 1:
        #         print(cls.vert + cls.horiz * 78 + cls.vert)
        #         continue
        #     elif _ == 20:
        #         print(cls.vert + cls.horiz * 78 + cls.vert)
        #         continue
        #     elif _ == 21:
        #         print('[B]ack'.center(38) + cls.vert + '[N]ext'.center(38))
        #     elif ootext:
        #         print(cls.vert + ' ' * 78 + cls.vert)
        #     else:
        #         try:
        #             print(cls.vert + f'{entry.contents[_ - 2]}' + cls.vert)
        #         except IndexError:
        #             ootext = True
        #
        # print(cls.bottom_left + cls.horiz * 78 + cls.bottom_right)

    @classmethod
    def draw_ticker_row(cls, row_contents: str = ' ' * 80, emoji=None) -> None:
        """Draw paper tape ticks, with contents centered within."""
        if not emoji:
            print(cls.circle, row_contents, cls.circle)
        else:
            print(EmojiUnicodes.bread, row_contents, EmojiUnicodes.bread)
        time.sleep(.75)


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


if __name__ == '__main__':
    print(ColorEscapeSequences.GREEN)
    Drawing.print_character_sprite('PANERA')
    Drawing.draw_ticker_row(emoji=True)
    Drawing.print_character_sprite('BREAD')