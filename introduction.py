"""A program introducing myself."""
import time

class EscapeSequences:
    """Enumerated ANSI escape sequences.

    I wasn't sure if using the standard library was OK, so I didn't use the enum builtin library. I would almost always
    handle data of this type with an enumeration to maintain uniqueness and prevent mutability.
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

class EmojiUnicodes:
    pass


def the_end():
    """There's a reason I'm a STEM major. This is about the extent of my artistic skills."""
    print(' ' + '-' * 20 + ' ')
    print('|' + ' ' * 7 + f"{EscapeSequences.RED}THE END{EscapeSequences.RESET}" +  ' ' * 7 + '|')
    print(' ' + '-' * 20 + ' ')
    for _ in range(31):
        time.sleep(.75)
        print('')

# def introduction():
#     pass

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
    main()