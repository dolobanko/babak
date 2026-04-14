import unittest

from hello import (
    VERSION,
    rot13_text,
    render_alternating,
    render_arcade,
    render_bracket,
    render_cinema,
    render_chevron,
    render_hologram,
    render_plaque,
    render_receipt,
    render_ribbon,
    render_snakecase,
    render_titlecase,
    render_ticket,
    greet,
    render_boxed_shadow,
    render_double_border,
    render_flipcase,
    render_mirror,
    render_postcard,
    render_quote,
    render_shadow,
    render_spaced,
    render_stairs,
    wrap_with_border,
)

class TestHello(unittest.TestCase):
    def test_version_defined(self):
        self.assertEqual(VERSION, "1.0.44")

    def test_rot13_text_round_trips(self):
        self.assertEqual(rot13_text(rot13_text("Hello, World!")), "Hello, World!")

    def test_rot13_text_preserves_non_letters(self):
        self.assertEqual(rot13_text("Hi123!"), "Uv123!")

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

    def test_render_shadow_offsets_multiline_copy(self):
        self.assertEqual(render_shadow("Hi\nYo"), "Hi\nYo\n Hi\n Yo")

    def test_render_flipcase_swaps_letter_case(self):
        self.assertEqual(render_flipcase("Hi, ALIce!"), "hI, aliCE!")

    def test_render_boxed_shadow_wraps_then_offsets_border(self):
        self.assertEqual(
            render_boxed_shadow("Hi"),
            "+----+\n| Hi |\n+----+\n +----+\n | Hi |\n +----+",
        )

    def test_render_postcard_centers_message_with_header_and_footer(self):
        self.assertEqual(
            render_postcard("Hi"),
            "+========================+\n|  Greetings From Babak  |\n|                        |\n|           Hi           |\n|                        |\n|  Wish you were here.   |\n+========================+",
        )

    def test_render_quote_prefixes_each_line(self):
        self.assertEqual(render_quote("Hi\nThere"), "> Hi\n> There")

    def test_render_quote_preserves_blank_lines(self):
        self.assertEqual(render_quote("Hi\n\nThere"), "> Hi\n> \n> There")

    def test_render_double_border_nests_ascii_frames(self):
        self.assertEqual(
            render_double_border("Hi"),
            "+--------+\n| +----+ |\n| | Hi | |\n| +----+ |\n+--------+",
        )

    def test_render_arcade_wraps_message_in_retro_scoreboard(self):
        self.assertEqual(
            render_arcade("Hi"),
            ".=============================.\n|         BABAK ARCADE        |\n|                             |\n|              Hi             |\n|                             |\n|  CREDITS: 01   PRESS START  |\n'============================='",
        )

    def test_render_ticket_wraps_message_in_ticket_stub(self):
        self.assertEqual(
            render_ticket("Hi"),
            ".-----------------.\n|    ADMIT ONE    |\n|-----------------|\n|        Hi       |\n|-----------------|\n|  BABAK EXPRESS  |\n'-----------------'",
        )

    def test_render_alternating_toggles_case_for_letters_only(self):
        self.assertEqual(render_alternating("Hello, World! 123"), "HeLlO, wOrLd! 123")

    def test_render_ribbon_wraps_message_in_banner(self):
        self.assertEqual(
            render_ribbon("Hi"),
            " /----\\\n< Hi >\n \\----/\n  \\\\  //",
        )

    def test_render_titlecase_capitalizes_words_per_line(self):
        self.assertEqual(render_titlecase("hello world\nfrom babak"), "Hello World\nFrom Babak")

    def test_render_plaque_displays_message_with_footer(self):
        self.assertEqual(
            render_plaque("Hi"),
            ".=============.\n|      Hi     |\n|  BABAK CLI  |\n'============='",
        )

    def test_render_snakecase_normalizes_words_and_hyphens(self):
        self.assertEqual(render_snakecase("Hello-There Babak"), "hello_there_babak")

    def test_render_chevron_wraps_each_line_with_markers(self):
        self.assertEqual(render_chevron("Hi\nYo"), ">> Hi <<\n>> Yo <<")

    def test_render_receipt_formats_message_like_printout(self):
        self.assertEqual(
            render_receipt("Hi"),
            "+-----------------+\n|  BABAK RECEIPT  |\n|-----------------|\n|  Hi             |\n|-----------------|\n|    THANK YOU    |\n+-----------------+",
        )

    def test_render_hologram_displays_scifi_panel(self):
        self.assertEqual(
            render_hologram("Hi"),
            ".====================.\n|  HOLOGRAM: ONLINE  |\n|  ~~~~~~~~~~~~~~~~  |\n|  > Hi              |\n|  ~~~~~~~~~~~~~~~~  |\n|   SIGNAL: LOCKED   |\n'===================='",
        )

    def test_render_cinema_displays_marquee(self):
        self.assertEqual(
            render_cinema("Hi"),
            "*================*\n|  NOW SHOWING   |\n|                |\n|       Hi       |\n|                |\n|  BABAK CINEMA  |\n*================*",
        )

    def test_render_bracket_wraps_each_line(self):
        self.assertEqual(render_bracket("Hi\nYo"), "[ Hi ]\n[ Yo ]")

if __name__ == "__main__":
    unittest.main()
