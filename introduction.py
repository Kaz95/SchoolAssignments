"""A program introducing myself.

TODO:
    * Move post title sleep outside of title function for better control.
    * Write 10 'Entries'.
    * Verify entry sizing.
    * Write new main function that reflects current state of program.
    * Come up with a better git workflow. Squashing conflicts too often working from laptop.

"""
import shutil, time, textwrap
import subprocess
import sys
from dataclasses import dataclass

TERMINAL_WIDTH, TERMINAL_HEIGHT = shutil.get_terminal_size()

ENTRY_CONTENTS = {'hemophilia': ("I was born with a genetic bleeding disorder called Hemophilia. I won't go into "
                                 "much detail here due to space constraints, but it generally manifests in swollen "
                                 "joints and muscles. It caused me to miss quite a bit of school in my late teens. "
                                 "It's also the reason I was not able to attend college until now. I've always wanted "
                                 "to continue my education after high school, but the state of my health just "
                                 "didn't allow it. Recently, the medicine I use to treat the condition has improved "
                                 "quite a bit and as a result I'm finally able to attend in-person classes. "
                                 "Honestly, I'm ecstatic everyday knowing I get to go to school."),

                  'age': ("I'm a non traditional student, with this being my first semester at 31."
                          "As I mentioned, I was unable to attend school for many years, and as a result I'm getting "
                          "a late start. It's hard not to feel like I'm already behind, even though I've just started. "
                          "Although, in some ways, I'm thankful to just be starting. I'm a much different person than "
                          "I was in my twenties. I feel like the person I am today is much better prepared for what's to "
                          "come."),

                  'ai': ("AI scares the absolute crap out of me. It is also among the coolest things I've been alive "
                         "to see the advent of. I believe one day this era will be looked at similar to the adoption "
                         "of stored program computers, or that first keyboard being introduced to the Whirl Wind project. "
                         "Its one of the largest shifts ever in how humans will interface with computers in the future."
                         "Its amazing at searching documentation, acting as a sounding board(rubber ducking), and "
                         "providing basic usage examples for 3rd party libraries APIs. I use it quite a bit for those "
                         "things specifically in the last few months. It can really save a lot of time in those tasks."
                         "All that being said, it still scares the crap out of me. It should scare anyone who's ever "
                         "written a line of code before its advent. I realized very quickly you can't use it for code "
                         "generation, if you want to learn anything anyway. You don't bring a forklift to the gym."
                         "As a result, I actually have little(no) experience with AI workflows or anything like that. "
                         "Tooling changes often, and I can always learn it later."),

                  'major': ("I'm currently working on an Associates in Engineering sciences transfer degree. "
                            "I plan to transfer to UIC under the TAG program. Originally, I intended to major in "
                            "Computer Science after my transfer, but a number of things pushed me towards Computer "
                            "Engineering. My aforementioned fear of AI definitely played a role. I'm worried about "
                            "what the average software focused role will look like when I graduate. I'm worried about "
                            "how many of those roles will exist. I've never been interested in front-end development "
                            "for the most part, so that eliminates many possible career paths. Over the last few "
                            "months, I've tried to distill my interests down to the point where I could better picture "
                            "what kind of job I may want some day. That process led me to Computer Engineering."),

                  'study': ("The areas I'm most interested in at the moment are embedded systems, FPGAs, and "
                            "networking. It occurred to me, I knew quite a bit about high level "
                            "programming(both functional and object oriented), but painfully little about much else in "
                            "the realm of computer science. So, I started learning C to learn about low level "
                            "memory management, and embedded systems. I started working on the nand2Tetris project to "
                            "learn about digital design. I'm currently wrestling with De Morgan's law and boolean "
                            "algebra. For networking, I'm learning about the OSI model and its various layers. These "
                            "areas of interest and all I've learned about them recently helped push me towards "
                            "Computer Engineering."),

                  'fishing': ("Outside of computer related things, I only have a few hobbies I really enjoy. One of "
                              "them is bass fishing. I like fishing in general, but Largemouth and Smallmouth Bass "
                              "are my favorites. I grew up fishing pretty casually with my family, but had been away "
                              "from it for some time. When my health started to improve I decided to try bass fishing "
                              "and got hooked(pun intended). One of the things I'm most looking forward to when I "
                              "start my career, will be purchasing my first bass boat. Oddly enough, bass fishing also "
                              "helped push me towards Computer Engineering. There's some cool work being done with "
                              "'Live Scope', a real time sonar system. There's work involving FPGAs, ASICs, and "
                              "embedded systems."),

                  'baseball': ("Another non computer related hobby of mine is baseball. I try to catch as many games "
                               "as I can on TV. I'm a White Sox fan, although I follow a number of other teams. My "
                               "favorite active player on the Sox is Sam Antonacci. I've rarely seen anyone do "
                               "much of anything in life with the effort he puts in every play. As I fan, I appreciate "
                               "that more than the result."),

                  'arcade': ("I've enjoyed video games as long as I can remember. My earliest memories include playing "
                             "Pac-man on my mom's Game Boy in her lap. They include me teaching myself how to use a "
                             "floppy drive so I could play old MS DOS games we acquired from who knows where. Arcade "
                             "games are my favorites. They are where I started(Pac-man/Galaga) and where I eventually "
                             "landed. Something about the simplicity of early 80s arcade games mixed with the "
                             "deceptive difficulty, makes them timeless. My love of arcade games is why I'm interested "
                             "in FPGAs. The MiSTer project, which attempts to recreate various arcade hardware using "
                             "FPGAs, is what drew me to them. This is one of the main things that pushed me towards "
                             "Computer Engineering as a major."),

                  'genres': ("My favorite genre across all forms of media, is scifi. I enjoy fantasy and historical "
                            "dramas, but scifi trounces everything else. My dad grew up on Star Trek, and he passed "
                            "it right on down to me. I've seen each of the Star Trek series more times than I care to "
                            "admit, with my favorite being Next Generation. I spend more time reading scifi, than "
                            "watching it nowadays. I've mostly been reading Star Trek and Star Wars lately, but "
                            "I'll read just about anything scifi if it catches my interest. Since this entry is about "
                            "genres of media I like, I'll finish with music. I like all types of music. Some of the "
                            "more unexpected genres I enjoy are country, 80s Japanese city pop, and Spanish guitar. "
                            "I've been listening to Andalusian Nights by Govi lately. Finding new music I enjoy is "
                            "one of the things I get the most joy out of."),

                  'computers': ("I love computers. I love absolutely everything about them. If you had asked for one "
                                "thing about myself, that's what I would have said. Its, by far, the most important. I "
                                "love programming, the history of them, the hardware, the theory. I love it all and I "
                                "want to know it all. They got me through the roughest parts of my life. Sometimes they "
                                "were my entertainment, other times they were my teacher. I met my two best friends "
                                "playing World of Warcraft when we were 12. They are going to be how I make my living."),

                  'thank_you': ("Well, thank you for reading all of that. I ended up enjoying this project quite a bit. "
                                "Sometimes its easier to learn about yourself by telling someone else, I suppose. I "
                                "think you've come up with a great class format. I was a bit harsh on the zybook "
                                "lessons at first, but I realized I needed to look through the eyes of a beginner. "
                                "The visual examples are really fantastic and would have been a great aid to me when "
                                "I started. I love that you allow us to work at our own pace. It allowed me to gauge "
                                "how much time I would be able to spend on this project. I spent the second half of one "
                                "of our lab days working on this project under a nice tree, in front of one of the "
                                "ponds on campus. I've never even programmed outside the house before. That was a "
                                "really nice day. So, thanks for the attendance policy! It allowed me to enjoy "
                                "something new. I'll close with a link to my github, where you will find my most "
                                "recent completed project, and my current project. The completed project is a full "
                                "stack desktop app I made to ease working with multiple versions of arcade game "
                                "emulators. My current project is my first attempt at making an emulator of my own."
                                "That project is where I got the idea for the 'bit-mapped' graphics in this project."
                                "If there are ever any opportunities you think I may be a good fit for, please let me "
                                "know. Tutoring, help desk, local internships; Whatever it is, I'm interseted.")

                  }




@dataclass()
class Entry:
    """A single entry."""
    ordinal: int
    subject: str
    emoji: str
    contents: list[str]


class Drawing:
    """Class that handles all drawing logic."""
    top_left = "\u250c"  # ┌
    top_right = "\u2510"  # ┐
    bottom_left = "\u2514"  # └
    bottom_right = "\u2518"  # ┘
    horiz = "\u2500"  # ─
    vert = "\u2502"  # │
    half_block = "\u2588"  # █
    circle = '\u2B24' # ⬤

    @classmethod
    def print_character_sprite(cls, word:str) -> None:
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
            row_string = row_string.center(TERMINAL_WIDTH)
            Drawing.draw_ticker_row(row_string)
        time.sleep(3)

    @classmethod
    def draw_window(cls, entry: Entry) -> None:
        """Draw a 'window' with boarder Unicode characters."""
        ootext = False
        print(cls.top_left + cls.horiz * 78 + cls.top_right)
        for _ in range(22):
            if _ == 0:
                subject = f'{entry.emoji} {entry.subject} {entry.emoji}'
                print(subject.center(80))
                continue
            elif _ == 1:
                print(cls.vert + cls.horiz * 78 + cls.vert)
                continue
            elif _ == 20:
                print(cls.vert + cls.horiz * 78 + cls.vert)
                continue
            elif _ == 21:
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
    def draw_ticker_row(cls, row_contents: str = ' ' * 80) -> None:
        """Draw paper tape ticks, with contents centered within."""
        print(cls.circle, row_contents, cls.circle)
        time.sleep(1)

class Entries:
    """Class to handle working with entries.

    Handles ordering based on ordinal, as well as printing.
    """
    current_entry = 0
    ENTRIES = []

    @classmethod
    def create_entry(cls, ordinal, subject, emoji, contents):
        cls.ENTRIES.append(Entry(ordinal, subject, emoji, contents))


    @classmethod
    def next_entry(cls) -> bool:
        """Move to next entry. Return false if last entry."""
        if (cls.current_entry + 1) >= len(cls.ENTRIES):
            return False
        else:
            cls.current_entry += 1
            return True

    @classmethod
    def prev_entry(cls) -> None:
        """Move to prev entry."""
        if (cls.current_entry - 1) <= 0:
            cls.current_entry = 0
        else:
            cls.current_entry -= 1

    @classmethod
    def print_entry(cls) -> None:
        """Print a single entry."""
        Drawing.draw_window(cls.ENTRIES[cls.current_entry])


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
    WHITE = "\033[37m"  # White
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
    briefcase = '1F4BC'
    robot = '1F916'

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
def clear_console() -> None:
    """Multi-platform console clear."""
    if sys.platform == 'win32':
        command = 'cls'
    else:
        command = 'clear'
    subprocess.run(command, shell=True)


# Not sure if the use of the '__main__' idiom for entry is OK? I created a main() function just incase.
# That way I (or you) only need to move one line.
if __name__ == '__main__':
    # main()

    Drawing.print_character_sprite('intro.py')
    Drawing.draw_ticker_row()
    Drawing.draw_ticker_row()
    Drawing.draw_ticker_row()
    Drawing.draw_ticker_row('Controls:'.center(terminal_width))
    Drawing.draw_ticker_row('[N]ext'.center(terminal_width))
    Drawing.draw_ticker_row('[B]ack'.center(terminal_width))
    Drawing.draw_ticker_row('[E]xit'.center(terminal_width))
    Drawing.draw_ticker_row('Press Enter to continue: '.center(terminal_width))
    input()
    clear_console()
    print(ColorEscapeSequences.PHOSPHORGREEN)

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
    baseball_entry = Entry(2, 'I really enjoy watching baseball.', EmojiUnicodes.baseball, test_text)
    prev_entry = Entry(1, 'A prev entry.', EmojiUnicodes.baseball, test_text)
    next_entry = Entry(3, 'A next entry.', EmojiUnicodes.baseball, test_text)
    # entries = [prev_entry, baseball_entry, next_entry]
    Entries.ENTRIES.append(baseball_entry)
    Entries.ENTRIES.append(prev_entry)
    Entries.ENTRIES.append(next_entry)
    Entries.ENTRIES.sort(key=lambda entry: entry.ordinal)
    Drawing.draw_window(Entries.ENTRIES[Entries.current_entry])

    while True:
        direction = input('? ')
        clear_console()

        if direction.lower() == 'b':
            Entries.prev_entry()

        else:
            if not Entries.next_entry():
                break

        Entries.print_entry()

    print(ColorEscapeSequences.RESET)
    Drawing.print_character_sprite('The end')