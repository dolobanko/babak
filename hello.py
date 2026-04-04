import argparse

VERSION = "1.0.4"

def greet(name="World", uppercase=False, greeting="Hello", quiet=False, reverse=False):
    """
    Generates a greeting message.
    """
    normalized_name = (name or "").strip() or "World"
    normalized_greeting = (greeting or "").strip() or "Hello"
    punctuation = "" if quiet else "!"
    message = f"{normalized_greeting}, {normalized_name}{punctuation}"
    if uppercase:
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
        "--version",
        action="version",
        version=f"%(prog)s {VERSION}",
    )
    args = parser.parse_args()
    message = greet(args.name, uppercase=args.uppercase, greeting=args.greeting, quiet=args.quiet, reverse=args.reverse)
    for _ in range(args.repeat):
        print(message)

if __name__ == "__main__":
    main()
