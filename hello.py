import argparse
from datetime import datetime

VERSION = "1.0.11"

COLORS = {
    "red": "\033[31m",
    "green": "\033[32m",
    "yellow": "\033[33m",
    "blue": "\033[34m",
    "magenta": "\033[35m",
    "cyan": "\033[36m",
}
RESET = "\033[0m"

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
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    args = parser.parse_args()
    message = greet(args.name, uppercase=args.uppercase, greeting=args.greeting, quiet=args.quiet, reverse=args.reverse, separator=args.separator, shout=args.shout)
    if args.timestamp:
        ts = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        message = f"[{ts}] {message}"
    output = f"{COLORS[args.color]}{message}{RESET}" if args.color else message
    if args.border:
        border_line = "+" + "-" * (len(message) + 2) + "+"
        output = f"{border_line}\n| {output} |\n{border_line}"
    for _ in range(args.repeat):
        print(output)
    if args.count:
        print(f"({len(message)} characters)")

if __name__ == "__main__":
    main()
