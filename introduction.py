"""A program introducing myself.

TODO:
    * Fill out docstrings
    * Come up with a better git workflow. Squashing conflicts too often working from laptop.
    * Write 10 print statements.
    * Improve end 'animation'. Maybe use Unicode 'blocks'
"""
import shutil, time, textwrap



terminal_size = shutil.get_terminal_size()
print(terminal_size)


class EscapeSequences:
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
    def __getattribute__(self, name: str, /):
        value = super().__getattribute__(name)

        # Block dunder methods.
        if name.startswith('__') and name.endswith('__'):
            return value
        else:
            new_val = fill_emoji_unicode(value)
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







def fill_emoji_unicode(emoji:str):
    split_emoji = emoji.split(r'\u')
    padded_code = rf'\U{split_emoji[0]:0>8}'
    print(padded_code)

    if len(split_emoji) > 1:
        padded_code = padded_code + rf'\u{split_emoji[1]}'

    # Learned some cool stuff about run-time vs compilation.
    # Need to manually decode. Dynamic string isn't available at compile time, and isn't recognized as an ANSI escape.
    emoji = padded_code.encode('utf-8').decode('unicode_escape')
    return emoji




def the_end():
    """There's a reason I'm a STEM major. This is about the extent of my artistic skills."""
    print(' ' + '-' * 20 + ' ')
    print('|' + ' ' * 7 + f"{EscapeSequences.RED}THE END{EscapeSequences.RESET}" +  ' ' * 7 + '|')
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
        print('Something about be and stuff, Something about be and stuff, Something about be and stuff, ')

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
    # main()
    # some_code = fill_emoji_unicode(EmojiUnicodes.fish)
    # print(some_code)
    emoji_code = EmojiUnicodes.clock
    print(emoji_code)
