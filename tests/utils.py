import unittest
from emmet import expand as expand_emmet
from bs4 import BeautifulSoup


class BaseEmmetTestCase(unittest.TestCase):
    maxDiff = None

    def reverse_debug(self, abbr: str):
        reversed_html = expand_emmet(abbr)
        print(f"\n\n{reversed_html}\n")

    def emmet_reverse_assert(self, expected_html: str, expected_abbr: str):
        """Assert that the reverse emmetified result is correct"""
        reversed_html = expand_emmet(expected_abbr)
        pretty_expected = BeautifulSoup(expected_html, "html.parser").prettify()
        pretty_reversed = BeautifulSoup(reversed_html, "html.parser").prettify()
        self.assertEqual(
            pretty_expected, pretty_reversed, "Reverse emmetified result is incorrect"
        )
