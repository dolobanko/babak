import unittest

from hello import VERSION, greet, render_mirror, render_spaced, render_stairs, wrap_with_border

class TestHello(unittest.TestCase):
    def test_version_defined(self):
        self.assertEqual(VERSION, "1.0.28")

    def test_greet_quiet(self):
        self.assertEqual(greet("Alice", quiet=True), "Hello, Alice")

    def test_greet_default(self):
        self.assertEqual(greet(), "Hello, World!")

    def test_greet_name(self):
        self.assertEqual(greet("Alice"), "Hello, Alice!")

    def test_greet_blank_name_falls_back_to_world(self):
        self.assertEqual(greet("   "), "Hello, World!")

    def test_greet_uppercase(self):
        self.assertEqual(greet("Alice", uppercase=True), "HELLO, ALICE!")

    def test_greet_custom_greeting(self):
        self.assertEqual(greet("Alice", greeting="Hi"), "Hi, Alice!")

    def test_greet_blank_greeting_falls_back_to_hello(self):
        self.assertEqual(greet("Alice", greeting="   "), "Hello, Alice!")

    def test_wrap_with_border_single_line(self):
        self.assertEqual(
            wrap_with_border("Hello, World!"),
            "+---------------+\n| Hello, World! |\n+---------------+",
        )

    def test_wrap_with_border_multiline_pads_shorter_lines(self):
        self.assertEqual(
            wrap_with_border("Hi\nHello"),
            "+-------+\n| Hi    |\n| Hello |\n+-------+",
        )

    def test_render_stairs_offsets_each_character(self):
        self.assertEqual(render_stairs("Hi!"), "H\n i\n  !")

    def test_render_mirror_adds_reversed_reflection(self):
        self.assertEqual(render_mirror("Hello"), "Hello\nolleH")

    def test_render_spaced_preserves_lines(self):
        self.assertEqual(render_spaced("Hi\nYo"), "H i\nY o")

if __name__ == "__main__":
    unittest.main()
