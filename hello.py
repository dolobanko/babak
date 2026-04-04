import argparse

VERSION = "1.0.2"

def greet(name="World", uppercase=False, greeting="Hello"):
    """
    Generates a greeting message.
    """
    normalized_name = (name or "").strip() or "World"
    normalized_greeting = (greeting or "").strip() or "Hello"
    message = f"{normalized_greeting}, {normalized_name}!"
    if uppercase:
        return message.upper()
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
    message = greet(args.name, uppercase=args.uppercase, greeting=args.greeting)
    for _ in range(args.repeat):
        print(message)

if __name__ == "__main__":
    main()
