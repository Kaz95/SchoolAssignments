"""A program introducing myself.

TODO:
    * Sketch a quick overview of overall program flow.
    * Start integration of new stuff and removal of deprecated code.
    * Fill out docstrings.
    * Fill out type hints.
    * Come up with a better git workflow. Squashing conflicts too often working from laptop.
    * Write 10 'Entries'.
"""
import shutil, time, textwrap
import subprocess
import sys
from dataclasses import dataclass

terminal_width, terminal_height = shutil.get_terminal_size()

@dataclass()
class Entries:
    ordinal: int
    subject: str
    emoji: str
    contents: list[str]


class Drawing:
    """Character codes used for drawing boarders."""
    top_left = "\u250c"  # ┌
    top_right = "\u2510"  # ┐
    bottom_left = "\u2514"  # └
    bottom_right = "\u2518"  # ┘
    horiz = "\u2500"  # ─
    vert = "\u2502"  # │
    half_block = "\u2588"  # █
    circle = '\u2B24' # ⬤

    @classmethod
    def print_character_sprite(cls, word):
        """Draw character sprite base on given sprite data."""
        # Need to double up to maintain square aspect ratio
        full_block = cls.half_block * 2
        double_space = "  "

        sprite_word = []
        for char in word:
            sprite_word.append(character_sprites[char])

        for _ in range(5):
            row_string = ''
            for char in sprite_word:
                row = f'{char[_]:05b}'
                graphic_row = ''.join(full_block if char == "1" else double_space for char in row)
                row_string += graphic_row
            row_string = row_string.center(terminal_width)
            # print('\u2B24', row_string, '\u2B24')
            # time.sleep(1)
            Drawing.draw_ticker_row(row_string)
        time.sleep(3)

    @classmethod
    def draw_window(cls, entry: Entries):
        ootext = False
        print(cls.top_left + cls.horiz * 78 + cls.top_right)
        for _ in range(23):
            if _ == 0:
                subject = f'{entry.emoji} {entry.subject} {entry.emoji}'
                print(subject.center(80))
                continue
            elif _ == 1:
                print(cls.vert + cls.horiz * 78 + cls.vert)
                continue
            elif _ == 21:
                print(cls.vert + cls.horiz * 78 + cls.vert)
                continue
            elif _ == 22:
                print('[B]ack'.center(38) + cls.vert + '[N]ext'.center(38))
            elif ootext:
                print(cls.vert + ' ' * 78 + cls.vert)
            else:
                try:
                    print(cls.vert + f'{entry.contents[_ - 2]}' + cls.vert)
                except IndexError:
                    ootext = True

        print(cls.bottom_left + cls.horiz * 78 + cls.bottom_right)

    @classmethod
    def draw_ticker_row(cls, row_contents=' ' * 80):
        print(cls.circle, row_contents, cls.circle)
        time.sleep(1)


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
    PHOSPHORGREEN = "\033[1;92m"  # Bold, High-Intensity green.


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
    print(
        Drawing.half_block + ' ' * 7 + f"{ColorEscapeSequences.RED}THE END{ColorEscapeSequences.RESET}" + ' ' * 7 + Drawing.half_block)
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


# def main():
#     for _ in range(11):
#         print(textwrap.fill('Something about me and stuff' * 10, width=80))
#
#     first_pass = True
#     while True:
#         if first_pass:
#             done = input('Are you finished reading? Y/N: ')
#             first_pass = False
#         else:
#             done = input('\nHow about now? Y/N: ')
#
#         if done.lower() == 'y':
#             the_end()
#             break
#
#         print('No problem. Take your time. I\'m going for a quick nap.')
#         for _ in range(16):
#             print('Z', end='')
#             time.sleep(1)

# def main() -> None:
#     """Main program entry."""
#     Drawing.print_character_sprite('intro.py')
#     Drawing.draw_ticker_row()
#     Drawing.draw_ticker_row()
#     # Drawing.draw_ticker_row()
#     Drawing.draw_ticker_row('Controls:'.center(terminal_width))
#     Drawing.draw_ticker_row('[N]ext'.center(terminal_width))
#     Drawing.draw_ticker_row('[B]back'.center(terminal_width))
#     Drawing.draw_ticker_row('[E]xit'.center(terminal_width))
#     Drawing.draw_ticker_row('Press Enter to continue: '.center(terminal_width))
#     input('? ')
    # TODO: Figure out I'm going to organize 'entries'. Probably a list or dict. List makes more sense.
    # Drawing.draw_window()
    # Print instructions
    # Open first entry w/ prompt for movement.



# TODO This pattern is straight from the docs and modified. Figure out why it said os is deprecated.
def clear_console():
    if sys.platform == 'win32':
        command = 'cls'
    else:
        command = 'clear'
    subprocess.run(command, shell=True)


# Not sure if the use of the '__main__' idiom for entry is OK? I created a main() function just incase.
# That way I (or you) only need to move one line.
if __name__ == '__main__':
    # main()
    # some_code = fill_emoji_unicode(EmojiUnicodes.fish)
    # print(some_code)
    # emoji_code = EmojiUnicodes.clock
    # print(emoji_code)
    # Drawing.print_character_sprite('intro.py')
    # print('')
    # Drawing.print_character_sprite('The end')

    test_data = """Lorem ipsum dolor sit amet, consectetuer adipiscing elit. Aenean commodo ligula eget dolor. Aenean 
    massa. Cum sociis natoque penatibus et magnis dis parturient montes, nascetur ridiculus mus. Donec quam felis, 
    ultricies nec, pellentesque eu, pretium quis, sem. Nulla consequat massa quis enim. Donec pede justo, 
    fringilla vel, aliquet nec, vulputate eget, arcu. In enim justo, rhoncus ut, imperdiet a, venenatis vitae, 
    justo. Nullam dictum felis eu pede mollis pretium. Integer tincidunt. Cras dapibus. Vivamus elementum semper 
    nisi. Aenean vulputate eleifend tellus. Aenean leo ligula, porttitor eu, consequat vitae, eleifend ac, 
    enim. Aliquam lorem ante, dapibus in, viverra quis, feugiat a, tellus. Phasellus viverra nulla ut metus varius 
    laoreet. Quisque rutrum. Aenean imperdiet. Etiam ultricies nisi vel augue. Curabitur ullamcorper ultricies nisi. 
    Nam eget dui. Etiam rhoncus. Maecenas tempus, tellus eget condimentum rhoncus, sem quam semper libero, 
    sit amet adipiscing sem neque sed ipsum. N"""

    # Quick fix to clean up dirty string spacing from copied in test data.
    test_data = ' '.join(test_data.split())

    # test_text = textwrap.dedent(test_data)
    # test_text = textwrap.wrap(test_text, width=78)
    test_text = textwrap.wrap(test_data, width=78)
    test_text = [line.ljust(78) for line in test_text]
    cur_entry = 0
    baseball_entry = Entries(2, 'I really enjoy watching baseball.', EmojiUnicodes.baseball, test_text)
    prev_entry = Entries(1, 'A prev entry.', EmojiUnicodes.baseball, test_text)
    next_entry = Entries(3, 'A next entry.', EmojiUnicodes.baseball, test_text)
    entries = [prev_entry, baseball_entry, next_entry]
    Drawing.draw_window(entries[cur_entry])

    while True:
        # Drawing.draw_window('I really enjoy watching baseball.', '\U000026BE', test_text)
        direction = input('? ')
        #
        clear_console()

        if direction.lower() == 'b':
            cur_entry -= 1
            if cur_entry < 0:
                cur_entry = 0

        else:
            cur_entry += 1
            if cur_entry > len(entries) - 1:
                cur_entry = len(entries) - 1
                print('The end.')
                break

        Drawing.draw_window(entries[cur_entry])
