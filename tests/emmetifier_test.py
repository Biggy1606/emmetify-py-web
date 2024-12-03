import unittest
from emmet import expand as expand_emmet
from bs4 import BeautifulSoup

from emmetify import Emmetifier
from emmetify.config.base_config import EmmetifierConfig


class BaseTestCase(unittest.TestCase):
    maxDiff = None

    def indent_debug(self, input_html: str):
        normal = Emmetifier(config=EmmetifierConfig(debug=False, indent=False))
        indented = Emmetifier(config=EmmetifierConfig(debug=False, indent=True))
        normal_result = normal.emmetify(input_html)["result"]
        indented_result = indented.emmetify(input_html)["result"]
        print(f"\n\nNormal:\n{normal_result}\n\nIndented:\n{indented_result}\n")

    def reverse_debug(self, abbr: str):
        reversed_html = expand_emmet(abbr)
        print(f"\n\n{reversed_html}\n")

    def reverse_assert(self, input_html: str, expected_abbr: str):
        reversed_html = expand_emmet(expected_abbr)
        pretty_input = BeautifulSoup(input_html, "html.parser").prettify()
        pretty_reversed = BeautifulSoup(reversed_html, "html.parser").prettify()
        print("\n\nInput:\n", pretty_input, "\n\nReversed:\n", pretty_reversed, "\n\n")
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
        expected_abbr = 'div#main.container[data-test=ignore]{Tytus Bomba}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)

    def test_multi_line_html(self):
        html = """<div id="main" class="container" data-test="ignore">
            Tytus Bomba
        </div>
        <div id="main" class="container" data-test="ignore">
            Tytus Bomba
        </div>"""
        expected_abbr = 'div#main.container[data-test=ignore]{Tytus Bomba}+div#main.container[data-test=ignore]{Tytus Bomba}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)

    def test_simple_nested_structure(self):
        html = """<nav class="menu">
            <ul>
                <li><a href="#home">Home</a></li>
            </ul>
        </nav>"""
        expected_abbr = 'nav.menu>ul>li>a[href=#home]{Home}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)

    def test_multiple_nested_structures(self):
        html = """<nav class="menu">
            <ul>
                <li id="no-children">
                </li>
                <li id="children">
                    <div id="2"></div>
                </li>
                <li><a href="#about">About</a></li>
            </ul>
            <div id="3"></div>
        </nav>"""
        expected_abbr = 'nav.menu>(ul>li#no-children+(li#children>div#2)+(li>a[href=#about]{About}))+div#3'
        self.emmet_assert(self.emmetifier, html, expected_abbr)

    def test_attributes_order(self):
        html = """<div id="main" class="container" data-test="ignore" data-test2="ignore2">
            Tytus Bomba
        </div><div id="main" class="container" data-test="ignore" data-test2="ignore2">
            Tytus Bomba
        </div>"""
        expected_abbr = 'div#main.container[data-test=ignore data-test2=ignore2]{Tytus Bomba}+div#main.container[data-test=ignore data-test2=ignore2]{Tytus Bomba}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)

    def test_attributes_with_spaces(self):
        html = """<div id="main" class="container" data-test="ignore" data-test2="ignore 2">
            Tytus Bomba
        </div><a href="https://example.com">Link</a>"""
        expected_abbr = 'div#main.container[data-test=ignore data-test2="ignore 2"]{Tytus Bomba}+a[href=https://example.com]{Link}'
        self.emmet_assert(self.emmetifier, html, expected_abbr)
