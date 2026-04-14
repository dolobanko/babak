import argparse
import math
import random
import sys
import time
from datetime import datetime

VERSION = "1.0.31"

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
    "ko": "Annyeong",
    "hi": "Namaste",
    "sv": "Hej",
    "tr": "Merhaba",
    "elvish": "Mae govannen",
    "pl": "Cześć",
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


ZALGO_MARKS = [chr(c) for c in range(0x0300, 0x036F)]


def zalgo_text(text, intensity=3):
    """Summon the cursed combining marks."""
    out = []
    for ch in text:
        out.append(ch)
        if ch.strip():
            for _ in range(random.randint(0, intensity)):
                out.append(random.choice(ZALGO_MARKS))
    return "".join(out)


def render_matrix(text, duration=2.0):
    """Matrix-style rain that resolves into the greeting."""
    GREEN = "\033[32m"
    BRIGHT_GREEN = "\033[92m"
    DIM_GREEN = "\033[2;32m"
    RESET_ALL = "\033[0m"
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_SCREEN = "\033[2J\033[H"

    width = max(len(line) for line in text.split("\n")) if "\n" in text else len(text)
    height = 20
    target_row = height // 2
    columns = list(range(width))
    random.shuffle(columns)

    # Each column has a rain drop falling; once it reaches target_row, it locks
    glyphs = "abcdefghijklmnopqrstuvwxyz0123456789@#$%&*<>{}[]!?/\\|~^"
    drops = {}  # col -> current row
    locked = {}  # col -> True once the char is revealed
    trail_len = 5

    for col in columns:
        drops[col] = random.randint(-height, -1)

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    fps = 30
    frames = int(duration * fps)
    try:
        for frame in range(frames):
            grid = [[" "] * width for _ in range(height)]

            for col in range(width):
                if col in locked:
                    if col < len(text):
                        grid[target_row][col] = text[col]
                    continue

                if col not in drops:
                    continue

                drop_row = drops[col]
                # Advance the drop
                drops[col] += 1

                if drops[col] >= target_row:
                    locked[col] = True
                    if col < len(text):
                        grid[target_row][col] = text[col]
                    continue

                # Draw the trail
                for t in range(trail_len + 1):
                    r = drop_row - t
                    if 0 <= r < height:
                        grid[r][col] = random.choice(glyphs)

            # Render
            buf = [CLEAR_SCREEN]
            for r in range(height):
                for c in range(width):
                    ch = grid[r][c]
                    if r == target_row and c in locked:
                        buf.append(f"{BRIGHT_GREEN}{ch}{RESET_ALL}")
                    elif ch != " ":
                        # Head of drop is bright, trail is dim
                        if c in drops and r == drops[c]:
                            buf.append(f"{BRIGHT_GREEN}{ch}{RESET_ALL}")
                        else:
                            buf.append(f"{DIM_GREEN}{ch}{RESET_ALL}")
                    else:
                        buf.append(" ")
                buf.append("\n")
            sys.stdout.write("".join(buf))
            sys.stdout.flush()
            time.sleep(1.0 / fps)

        # Final frame: show just the text clean
        sys.stdout.write(CLEAR_SCREEN)
        # Center the text vertically
        for _ in range(target_row):
            sys.stdout.write("\n")
        sys.stdout.write(f"{BRIGHT_GREEN}{text}{RESET_ALL}\n")
        sys.stdout.flush()
        time.sleep(0.5)
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


def render_fire(text, duration=3.0):
    """Animated fire effect — text burns with rising flames."""
    HIDE_CURSOR = "\033[?25l"
    SHOW_CURSOR = "\033[?25h"
    CLEAR_SCREEN = "\033[2J\033[H"
    RESET_ALL = "\033[0m"

    # Fire palette: black -> red -> orange -> yellow -> bright yellow -> white
    FIRE_COLORS = [
        "\033[30m",       # black (empty)
        "\033[2;31m",     # dim red
        "\033[31m",       # red
        "\033[91m",       # bright red
        "\033[33m",       # orange/yellow
        "\033[93m",       # bright yellow
        "\033[97m",       # white hot
    ]
    FIRE_CHARS = [" ", ".", ":", "*", "#", "%", "@", "&", "█", "▓", "▒", "░"]
    EMBER_CHARS = [".", "'", "`", "*", "^", "~"]

    width = len(text) + 4
    flame_height = 10
    text_row = flame_height + 1
    total_height = text_row + 3
    # Heat source: each column under a non-space char is hot
    heat_src = [1 if i - 2 < len(text) and i - 2 >= 0 and text[i - 2] != " " else 0 for i in range(width)]

    # Heat grid: [row][col] float 0..1
    heat = [[0.0] * width for _ in range(total_height)]

    sys.stdout.write(HIDE_CURSOR)
    sys.stdout.flush()

    fps = 20
    frames = int(duration * fps)
    try:
        for frame in range(frames):
            # Set heat sources at text row
            for c in range(width):
                if heat_src[c]:
                    heat[text_row][c] = min(1.0, 0.7 + random.random() * 0.3)
                    if text_row + 1 < total_height:
                        heat[text_row + 1][c] = min(1.0, 0.4 + random.random() * 0.3)

            # Propagate heat upward with cooling and spread
            new_heat = [[0.0] * width for _ in range(total_height)]
            for r in range(total_height):
                for c in range(width):
                    if r >= text_row:
                        new_heat[r][c] = heat[r][c]
                        continue
                    # Average from below + neighbors, with cooling
                    samples = []
                    for dr in [1, 2]:
                        if r + dr < total_height:
                            samples.append(heat[r + dr][c])
                    for dc in [-1, 1]:
                        if 0 <= c + dc < width and r + 1 < total_height:
                            samples.append(heat[r + 1][c + dc] * 0.5)
                    if samples:
                        avg = sum(samples) / len(samples)
                    else:
                        avg = 0
                    cooling = 0.06 + random.random() * 0.08
                    flicker = (random.random() - 0.5) * 0.1
                    new_heat[r][c] = max(0, min(1, avg - cooling + flicker))
            heat = new_heat

            # Render
            buf = [CLEAR_SCREEN]
            # Flame rows
            for r in range(flame_height):
                for c in range(width):
                    h = heat[r][c]
                    if h < 0.05:
                        buf.append(" ")
                    else:
                        ci = min(len(FIRE_COLORS) - 1, int(h * len(FIRE_COLORS)))
                        if h > 0.6:
                            ch = random.choice(FIRE_CHARS[6:])
                        elif h > 0.3:
                            ch = random.choice(FIRE_CHARS[3:7])
                        else:
                            ch = random.choice(FIRE_CHARS[:4])
                        buf.append(f"{FIRE_COLORS[ci]}{ch}{RESET_ALL}")
                buf.append("\n")

            # Ember row (sparks flying up)
            for c in range(width):
                if heat_src[c] and random.random() < 0.15:
                    buf.append(f"\033[93m{random.choice(EMBER_CHARS)}{RESET_ALL}")
                else:
                    buf.append(" ")
            buf.append("\n")

            # Text row — white hot
            buf.append("  ")
            for ch in text:
                glow = random.choice(["\033[97m", "\033[93m", "\033[91m"])
                buf.append(f"{glow}{ch}{RESET_ALL}")
            buf.append("\n")

            # Ash/coal row below text
            buf.append("  ")
            for i in range(len(text)):
                if random.random() < 0.7:
                    buf.append(f"\033[2;31m{random.choice(['_', '.', ','])}{RESET_ALL}")
                else:
                    buf.append(" ")
            buf.append("\n")

            sys.stdout.write("".join(buf))
            sys.stdout.flush()
            time.sleep(1.0 / fps)

        # Final clean frame
        sys.stdout.write(CLEAR_SCREEN)
        for _ in range(flame_height // 2):
            sys.stdout.write("\n")
        sys.stdout.write(f"  \033[93m🔥 {text} 🔥{RESET_ALL}\n")
        sys.stdout.flush()
        time.sleep(0.5)
    finally:
        sys.stdout.write(SHOW_CURSOR)
        sys.stdout.flush()


def render_wave(text, amplitude=2, wavelength=6):
    """Lay out text along a sine wave so characters ride up and down."""
    if not text:
        return text
    height = amplitude * 2 + 1
    grid = [[" "] * len(text) for _ in range(height)]
    for i, ch in enumerate(text):
        offset = round(amplitude * math.sin(2 * math.pi * i / wavelength))
        row = amplitude - offset
        grid[row][i] = ch
    return "\n".join("".join(row).rstrip() for row in grid)


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


def render_stairs(text):
    """Render characters diagonally so the text descends like stairs."""
    return "\n".join((" " * i) + ch for i, ch in enumerate(text))


def render_mirror(text):
    """Render the text and its reversed reflection on the next line."""
    return f"{text}\n{text[::-1]}"


def render_spaced(text):
    """Insert spaces between characters while preserving line breaks."""
    return "\n".join(" ".join(line) for line in text.split("\n"))


def render_shadow(text):
    """Print the text followed by a one-space-offset shadow copy."""
    lines = text.split("\n")
    shadow = "\n".join(f" {line}" for line in lines)
    return f"{text}\n{shadow}"


def render_flipcase(text):
    """Swap uppercase and lowercase characters while leaving other chars intact."""
    return "".join(ch.lower() if ch.isupper() else ch.upper() if ch.islower() else ch for ch in text)


def render_boxed_shadow(text):
    """Wrap the text in a border and add a shadow line beneath each row."""
    bordered = wrap_with_border(text)
    shadow = "\n".join(f" {line}" for line in bordered.split("\n"))
    return f"{bordered}\n{shadow}"


def render_postcard(text):
    """Lay out the greeting like a small ASCII postcard."""
    lines = text.split("\n")
    title = "Greetings From Babak"
    footer = "Wish you were here."
    width = max(len(line) for line in [*lines, title, footer])
    border = "+" + "=" * (width + 4) + "+"
    body = [
        border,
        f"|  {title.center(width)}  |",
        f"|  {' ' * width}  |",
    ]
    body.extend(f"|  {line.center(width)}  |" for line in lines)
    body.extend(
        [
            f"|  {' ' * width}  |",
            f"|  {footer.center(width)}  |",
            border,
        ]
    )
    return "\n".join(body)


def wrap_with_border(text):
    """Wrap single-line or multi-line text in an ASCII border."""
    lines = text.split("\n")
    width = max(len(line) for line in lines)
    border_line = "+" + "-" * (width + 2) + "+"
    body = "\n".join(f"| {line.ljust(width)} |" for line in lines)
    return f"{border_line}\n{body}\n{border_line}"

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
        "--zalgo",
        action="store_true",
        help="Summon cursed combining marks over the greeting.",
    )
    parser.add_argument(
        "--wave",
        action="store_true",
        help="Arrange characters along a sine wave.",
    )
    parser.add_argument(
        "--matrix",
        action="store_true",
        help="Matrix-style rain animation that resolves into the greeting.",
    )
    parser.add_argument(
        "--fire",
        action="store_true",
        help="Animated fire effect — text burns with rising flames.",
    )
    parser.add_argument(
        "--underline",
        action="store_true",
        help="Print a dashed line under the greeting (width matches the longest line).",
    )
    parser.add_argument(
        "--stairs",
        action="store_true",
        help="Render the greeting diagonally, one character per line.",
    )
    parser.add_argument(
        "--mirror",
        action="store_true",
        help="Print the greeting and a reversed reflection on the next line.",
    )
    parser.add_argument(
        "--spaced",
        action="store_true",
        help="Insert spaces between characters for a stretched-out look.",
    )
    parser.add_argument(
        "--shadow",
        action="store_true",
        help="Print the greeting with a one-space-offset shadow underneath.",
    )
    parser.add_argument(
        "--flipcase",
        action="store_true",
        help="Swap uppercase and lowercase characters in the greeting.",
    )
    parser.add_argument(
        "--boxed-shadow",
        action="store_true",
        help="Wrap the greeting in a border and print a shadow copy underneath.",
    )
    parser.add_argument(
        "--postcard",
        action="store_true",
        help="Display the greeting as a tiny ASCII postcard.",
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
    if args.zalgo:
        message = zalgo_text(message)
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
    if args.matrix:
        render_matrix(message)
        return
    if args.fire:
        render_fire(message)
        return
    if args.wave:
        message = render_wave(message)
    if args.stairs:
        message = render_stairs(message)
    if args.mirror:
        message = render_mirror(message)
    if args.spaced:
        message = render_spaced(message)
    if args.shadow:
        message = render_shadow(message)
    if args.flipcase:
        message = render_flipcase(message)
    if args.boxed_shadow:
        message = render_boxed_shadow(message)
    if args.postcard:
        message = render_postcard(message)
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
        output = wrap_with_border(output)
    for _ in range(args.repeat):
        print(output)
    if args.count:
        print(f"({len(message)} characters)")

if __name__ == "__main__":
    main()
