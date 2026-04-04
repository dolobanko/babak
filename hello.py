import argparse

def greet(name="World", uppercase=False):
    normalized_name = (name or "").strip() or "World"
    message = f"Hello, {normalized_name}!"
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
    args = parser.parse_args()
    print(greet(args.name, uppercase=args.uppercase))

if __name__ == "__main__":
    main()
