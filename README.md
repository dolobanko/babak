# Babak Project

Last updated: Tue Apr 14 2026

Testing branch policies for origin.

This repository is used for small CLI and workflow experiments.

## Scripts

- `hello.py` — CLI greeter with optional name argument, `--uppercase` mode, a custom `--greeting`, `--color` output, `--timestamp` to prepend the current time, `--border` support for both single-line and multi-line output, `--shadow` for a simple offset echo, `--flipcase` to invert letter case, `--boxed-shadow` for a bordered drop-shadow variant, `--postcard` for a postcard-style layout, `--arcade` for a retro cabinet screen, `--ticket` for a ticket-stub layout, `--titlecase` for capitalized words, `--snakecase` for underscored lowercase text, `--chevron` for a pointed callout wrapper, `--receipt` for a receipt-style printout, and a `--version` flag
- `hello_world.py` — simple Hello World entry point
- `test_hello.py` — unit tests for the greeter

## Usage

```bash
python hello.py
python hello.py Alice
python hello.py Alice --uppercase
python hello.py Alice --greeting Hi
python hello.py Alice --color cyan
python hello.py Alice --timestamp
python hello.py Alice --shadow
python hello.py Alice --flipcase
python hello.py Alice --boxed-shadow
python hello.py Alice --postcard
python hello.py Alice --arcade
python hello.py Alice --ticket
python hello.py "hello from babak" --titlecase
python hello.py "Hello-There Babak" --snakecase
python hello.py Alice --chevron
python hello.py Alice --receipt
python hello.py --version
python hello_world.py
```
