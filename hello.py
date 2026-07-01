import argparse


def greet(name="World"):
    clean_name = name.strip() or "World"
    return f"Hello, {clean_name}!"


def main():
    parser = argparse.ArgumentParser(description="A simple Hello World CLI app.")
    parser.add_argument("name", nargs="?", default="World", help="The name to greet.")
    args = parser.parse_args()
    print(greet(args.name))


if __name__ == "__main__":
    main()
