import argparse
import random
from datetime import datetime

VERSION = "1.0.19"

LANG_GREETINGS = {
    "en": "Hello",
    "es": "Hola",
    "fr": "Bonjour",
    "de": "Hallo",
    "it": "Ciao",
    "pt": "Olá",
    "ja": "Konnichiwa",
    "zh": "Ni hao",
    "ar": "Marhaba",
    "ru": "Privet",
    "lol": "OH HAI",
    "pirate": "Ahoy",
    "binary": "01001000 01101001",
}

OWL_ASCII = r"""
   ,___,
   [O.o]
   /)__)
  -"--"-"""

STICK_FIGURE = r"""
    o
   /|\
   / \
"""

GLITCH_MAP = str.maketrans("aeiosltAEIOSLT", "43101574310157")

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}
RESET = "\033[0m"

BLOCK_LETTERS = {
    'A': ["  #  ", " # # ", "#####", "#   #", "#   #"],
    'B': ["#### ", "#   #", "#### ", "#   #", "#### "],
    'C': [" ####", "#    ", "#    ", "#    ", " ####"],
    'D': ["#### ", "#   #", "#   #", "#   #", "#### "],
    'E': ["#####", "#    ", "###  ", "#    ", "#####"],
    'F': ["#####", "#    ", "###  ", "#    ", "#    "],
    'G': [" ####", "#    ", "# ###", "#   #", " ####"],
    'H': ["#   #", "#   #", "#####", "#   #", "#   #"],
    'I': ["#####", "  #  ", "  #  ", "  #  ", "#####"],
    'J': ["#####", "    #", "    #", "#   #", " ### "],
    'K': ["#   #", "#  # ", "###  ", "#  # ", "#   #"],
    'L': ["#    ", "#    ", "#    ", "#    ", "#####"],
    'M': ["#   #", "## ##", "# # #", "#   #", "#   #"],
    'N': ["#   #", "##  #", "# # #", "#  ##", "#   #"],
    'O': [" ### ", "#   #", "#   #", "#   #", " ### "],
    'P': ["#### ", "#   #", "#### ", "#    ", "#    "],
    'Q': [" ### ", "#   #", "# # #", "#  ##", " ####"],
    'R': ["#### ", "#   #", "#### ", "#  # ", "#   #"],
    'S': [" ####", "#    ", " ### ", "    #", "#### "],
    'T': ["#####", "  #  ", "  #  ", "  #  ", "  #  "],
    'U': ["#   #", "#   #", "#   #", "#   #", " ### "],
    'V': ["#   #", "#   #", " # # ", " # # ", "  #  "],
    'W': ["#   #", "#   #", "# # #", "## ##", "#   #"],
    'X': ["#   #", " # # ", "  #  ", " # # ", "#   #"],
    'Y': ["#   #", " # # ", "  #  ", "  #  ", "  #  "],
    'Z': ["#####", "   # ", "  #  ", " #   ", "#####"],
    ' ': ["     ", "     ", "     ", "     ", "     "],
    '!': ["  #  ", "  #  ", "  #  ", "     ", "  #  "],
    ',': ["     ", "     ", "     ", "  #  ", " #   "],
}

def apply_chaos(args):
    """Roll the dice on flags so no two runs feel the same."""
    r = random.random
    if r() < 0.55:
        args.emoji = True
    if r() < 0.4:
        args.timestamp = True
    if r() < 0.35:
        args.reverse = True
    if r() < 0.3:
        args.shout = True
    if r() < 0.45:
        args.border = True
    if r() < 0.25:
        args.quiet = True
    if r() < 0.2:
        args.uppercase = True
    if r() < 0.15:
        args.figlet = True
    if r() < 0.5:
        args.rainbow = True
        args.color = None
    elif r() < 0.35:
        args.color = random.choice(list(COLORS.keys()))
        args.rainbow = False


def glitch_text(text, intensity=0.35):
    """Leet-speak a random subset of eligible letters."""
    out = []
    for ch in text:
        if ch in GLITCH_MAP and random.random() < intensity:
            out.append(ch.translate(GLITCH_MAP))
        else:
            out.append(ch)
    return "".join(out)


def render_speech_bubble(text):
    width = len(text) + 2
    top = " " + "_" * width
    bottom = " " + "-" * width
    bubble = f"{top}\n< {text} >\n{bottom}"
    return bubble + "\n" + STICK_FIGURE.strip("\n")


def render_block(text):
    lines = [""] * 5
    for ch in text.upper():
        letter = BLOCK_LETTERS.get(ch, ["?????"] * 5)
        for i in range(5):
            lines[i] += letter[i] + " "
    return "\n".join(lines)

def greet(name="World", uppercase=False, greeting="Hello", quiet=False, reverse=False, separator=", ", shout=False):
    """
    Generates a greeting message.
    """
    normalized_name = (name or "").strip() or "World"
    normalized_greeting = (greeting or "").strip() or "Hello"
    punctuation = "" if quiet else "!"
    message = f"{normalized_greeting}{separator}{normalized_name}{punctuation}"
    if shout:
        message = message.upper() + "!!!"
    elif uppercase:
        message = message.upper()
    if reverse:
        message = message[::-1]
    return message

def main():
    parser = argparse.ArgumentParser(description="A simple Hello World CLI app.")
    parser.add_argument("name", nargs="?", default="World", help="The name to greet.")
    parser.add_argument(
        "--uppercase",
        action="store_true",
        help="Print the greeting in uppercase.",
    )
    parser.add_argument(
        "--greeting",
        default="Hello",
        help="Customize the greeting prefix.",
    )
    parser.add_argument(
        "--quiet",
        action="store_true",
        help="Omit the exclamation mark.",
    )
    parser.add_argument(
        "--reverse",
        action="store_true",
        help="Print the greeting reversed.",
    )
    parser.add_argument(
        "--repeat",
        type=int,
        default=1,
        help="Number of times to repeat the greeting.",
    )
    parser.add_argument(
        "--separator",
        default=", ",
        help="Separator between greeting and name (default: ', ').",
    )
    parser.add_argument(
        "--shout",
        action="store_true",
        help="Print the greeting in uppercase with extra exclamation marks.",
    )
    parser.add_argument(
        "--count",
        action="store_true",
        help="Show the character count of the greeting.",
    )
    parser.add_argument(
        "--color",
        choices=list(COLORS.keys()),
        help="Colorize the greeting output.",
    )
    parser.add_argument(
        "--border",
        action="store_true",
        help="Wrap the greeting in a decorative border.",
    )
    parser.add_argument(
        "--timestamp",
        action="store_true",
        help="Prepend the current date and time to the greeting.",
    )
    parser.add_argument(
        "--emoji",
        action="store_true",
        help="Prepend a random emoji to the greeting.",
    )
    parser.add_argument(
        "--figlet",
        action="store_true",
        help="Render the greeting in large ASCII block letters.",
    )
    parser.add_argument(
        "--rainbow",
        action="store_true",
        help="Print each character in a cycling rainbow color.",
    )
    parser.add_argument(
        "--lang",
        choices=list(LANG_GREETINGS.keys()),
        help="Greet in a specific language (overrides --greeting).",
    )
    parser.add_argument(
        "--chaos",
        action="store_true",
        help="Randomize emoji, colors, borders, and other flair each run.",
    )
    parser.add_argument(
        "--glitch",
        action="store_true",
        help="Corrupt some letters into l33t speak (stochastic).",
    )
    parser.add_argument(
        "--owl",
        action="store_true",
        help="Summon a tiny ASCII owl before the greeting.",
    )
    parser.add_argument(
        "--sparkle",
        action="store_true",
        help="Wrap the greeting with sparkle decorations.",
    )
    parser.add_argument(
        "--bubble",
        action="store_true",
        help="Display the greeting in a speech bubble with a stick figure.",
    )
    parser.add_argument(
        "--underline",
        action="store_true",
        help="Print a dashed line under the greeting (width matches the longest line).",
    )
    parser.add_argument(
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    args = parser.parse_args()
    if args.chaos:
        apply_chaos(args)
    greeting = LANG_GREETINGS[args.lang] if args.lang else args.greeting
    message = greet(args.name, uppercase=args.uppercase, greeting=greeting, quiet=args.quiet, reverse=args.reverse, separator=args.separator, shout=args.shout)
    if args.glitch:
        message = glitch_text(message)
    if args.timestamp:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{ts}] {message}"
    if args.owl:
        message = OWL_ASCII.strip("\n") + "\n" + message
    if args.emoji:
        emojis = ["👋", "🎉", "🌟", "🚀", "✨", "😊", "🔥", "💡", "🎯", "🌈"]
        message = f"{random.choice(emojis)} {message}"
    if args.figlet:
        message = render_block(message)
    if args.sparkle:
        message = f".:*~*:._.:*~*:. {message} .:*~*:._.:*~*:."
    if args.bubble:
        message = render_speech_bubble(message)
    if args.rainbow:
        rainbow_colors = list(COLORS.values())
        colored_chars = []
        for i, ch in enumerate(message):
            colored_chars.append(f"{rainbow_colors[i % len(rainbow_colors)]}{ch}{RESET}")
        output = "".join(colored_chars)
    elif args.color:
        output = f"{COLORS[args.color]}{message}{RESET}"
    else:
        output = message
    if args.underline:
        width = max(len(line) for line in message.split("\n"))
        output = output + "\n" + ("-" * width)
    if args.border:
        border_line = "+" + "-" * (len(message) + 2) + "+"
        output = f"{border_line}\n| {output} |\n{border_line}"
    for _ in range(args.repeat):
        print(output)
    if args.count:
        print(f"({len(message)} characters)")

if __name__ == "__main__":
    main()
