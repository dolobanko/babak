import unittest
from hello import greet

class TestHello(unittest.TestCase):
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

if __name__ == "__main__":
    unittest.main()
