import unittest
from emmet import expand as expand_emmet
from bs4 import BeautifulSoup

from emmetify import Emmetifier
from emmetify.config.base_config import EmmetifierConfig


class BaseTestCase(unittest.TestCase):
    maxDiff = None

    def indent_debug(self, input_html: str):
        indented = Emmetifier(config=EmmetifierConfig(debug=False, indent=True))
        result = indented.emmetify(input_html)["result"]
        print(f"\n\n{result}\n")

    def reverse_assert(self, input_html: str, expected_abbr: str):
        reversed_html = expand_emmet(expected_abbr)
        pretty_input = BeautifulSoup(input_html, "html.parser").prettify()
        pretty_reversed = BeautifulSoup(reversed_html, "html.parser").prettify()
        self.assertEqual(
            pretty_input, pretty_reversed, "Reverse emmetified result is incorrect"
        )

    def emmet_assert(self, emmetifier: Emmetifier, input_html: str, expected_abbr: str):
        """Assert that the emmetified result is correct and that the reverse is correct"""
        self.assertEqual(
            expected_abbr,
            emmetifier.emmetify(input_html)["result"],
            "Emmetified result is incorrect",
        )
        self.reverse_assert(input_html, expected_abbr)


class TestEmmetifierNoOptimization(BaseTestCase):
    def setUp(self):
        self.emmetifier = Emmetifier(config=EmmetifierConfig(debug=False, indent=False))

    def test_single_line_html(self):
        html = '<div id="main" class="container" data-test="ignore">Tytus Bomba</div>'
        expected_abbr = 'div#main.container[data-test="ignore"]{Tytus Bomba}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)

    def test_multi_line_html(self):
        html = """<div id="main" class="container" data-test="ignore">
            Tytus Bomba
        </div>
        <div id="main" class="container" data-test="ignore">
            Tytus Bomba
        </div>"""
        expected_abbr = 'div#main.container[data-test="ignore"]{Tytus Bomba}+div#main.container[data-test="ignore"]{Tytus Bomba}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)
