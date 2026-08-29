"""A program introducing myself.

TODO:
    * Sketch a quick overview of overall program flow.
    * Write prototype sprite drawing logic
    * Write prototype boarder drawing logic
    * Write prototype 'Journal' entry boarder logic
    * Fill out docstrings
    * Come up with a better git workflow. Squashing conflicts too often working from laptop.
    * Write 10 print statements.
    * Improve end 'animation'. Maybe use Unicode 'blocks'
"""
import shutil, time, textwrap



terminal_width, terminal_height = shutil.get_terminal_size()



class Drawing:
    """Character codes used for drawing boarders."""
    top_left = "\u250c"  # ┌
    top_right = "\u2510"  # ┐
    bottom_left = "\u2514"  # └
    bottom_right = "\u2518"  # ┘
    horiz = "\u2500"  # ─
    vert = "\u2502"  # │
    half_block = "\u2588"  # █

    def __init__(self):
        """I don't think I'll end up needing an init, as I won't be using instances.

        This is a bit of a new situation for me. I don't need to customize the class unless I want to customize some
        aspect of drawing, and I don't think I do, currently.
        """
        pass

    def print_character_sprite(self, character):
        """Draw character sprite base on given sprite data."""
        pass

    def draw_boarded_text(self, text):
        """Draw boarders around given text. May want to add dimension customization later.

        In the future, I may also want to add another method that draws a large standard size boarder. So this would
        handle small non-standard text elements, while the second method would handle a singe large standard text
        element. Something like drawing a single journal entry.
        """
        pass

character_sprites = {'T': [0xE, 0x4, 0x4, 0x4, 0x4],
                     't': [0x4, 0xE, 0x4, 0x4, 0x4],
                     'h': [0xA, 0xA, 0xE, 0xA, 0xA],
                     'e': [0xE, 0x8, 0xE, 0x8, 0xE],
                     'n': [0xE, 0xA, 0xA, 0xA, 0xA],
                     'd': [0xC, 0xA, 0xA, 0xA, 0xC],
                     ' ': [0x0, 0x0, 0x0, 0x0, 0x0],
                     'i': [0x4, 0x4, 0x4, 0x4, 0x4],
                     'r': [0xE, 0xA, 0x8, 0x8, 0x8],
                     'o': [0xE, 0xA, 0xA, 0xA, 0xE],
                     '.': [0x0, 0x0, 0x0, 0x0, 0x4],
                     'p': [0xE, 0xA, 0xE, 0x8, 0x8],
                     'y': [0xA, 0xA, 0xE, 0x4, 0x4]}

class ColorEscapeSequences:
    """Enumerated ANSI escape sequences.

    I wasn't sure if I wanted to use the actual enum module or not. This type of data is a perfect fit for an enum, but
    there is no reason to maintain uniqueness and immutability for this small project. I decided an enum would only
    make access more verbose, with none of the normal benefits.
    """
    RESET = "\033[0m"
    BLACK = "\033[30m"  # Black
    RED = "\033[31m"  # Red
    GREEN = "\033[32m"  # Green
    YELLOW = "\033[33m"  # Yellow
    BLUE = "\033[34m"  # Blue
    MAGENTA = "\033[35m"  # Magenta
    CYAN = "\033[36m"  # Cyan
    WHITE = "\033[37m"  # White
    BOLDBLACK = "\033[1m\033[30m"  # Bold Black
    BOLDRED = "\033[1m\033[31m"  # Bold Red
    BOLDGREEN = "\033[1m\033[32m"  # Bold Green
    BOLDYELLOW = "\033[1m\033[33m"  # Bold Yellow
    BOLDBLUE = "\033[1m\033[34m"  # Bold Blue
    BOLDMAGENTA = "\033[1m\033[35m"  # Bold Magenta
    BOLDCYAN = "\033[1m\033[36m"  # Bold Cyan
    BOLDWHITE = "\033[1m\033[37m"  # Bold White

# First time actually finding a solid use case for a MetaClass!
class PadZeroMeta(type):
    # Trying to add this to class or references just about any way other than class level static method causes recursion
    # I mostly understand why, but I need to look into it more. TODO: Fully understand class lookup.
    @staticmethod
    def fill_emoji_unicode(emoji: str):
        split_emoji = emoji.split(r'\u')
        padded_code = rf'\U{split_emoji[0]:0>8}'
        print(padded_code)

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
    blood = '1FA78'
    clock = r'1F570\uFE0F'
    programmer = '1F4BE'
    computer = r'1F5A5\uFE0F'
    fish = '1F3A3'
    baseball = '26BE'
    joystick = r'1F579\uFE0F'
    planet = '1F30C'
    briefcase = '1F4BC'

def the_end():
    """There's a reason I'm a STEM major. This is about the extent of my artistic skills."""
    print(' ' + '-' * 20 + ' ')
    print(full_block + ' ' * 7 + f"{EscapeSequences.RED}THE END{EscapeSequences.RESET}" +  ' ' * 7 + full_block)
    print(' ' + '-' * 20 + ' ')
    for _ in range(31):
        time.sleep(.75)
        print('')

def introduction():
    pass
    # Hemophilia
    # Age
    # Programming
    # Major
    # Study Interests
    # Fishing
    # Baseball
    # Arcade Games
    # Media Genres
    # Job

def main():
    for _ in range(11):
        print(textwrap.fill('Something about me and stuff' * 10, width=80))

    first_pass = True
    while True:
        if first_pass:
            done = input('Are you finished reading? Y/N: ')
            first_pass = False
        else:
            done = input('\nHow about now? Y/N: ')

        if done.lower() == 'y':
            the_end()
            break

        print('No problem. Take your time. I\'m going for a quick nap.')
        for _ in range(16):
            print('Z', end='')
            time.sleep(1)

# Not sure if the use of the '__main__' idiom for entry is OK? I created a main() function just incase.
# That way I (or you) only need to move one line.
if __name__ == '__main__':
    main()
    # some_code = fill_emoji_unicode(EmojiUnicodes.fish)
    # print(some_code)
    emoji_code = EmojiUnicodes.clock
    print(emoji_code)
