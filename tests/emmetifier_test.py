import unittest
from emmet import expand as expand_emmet
from bs4 import BeautifulSoup

from emmetify import Emmetifier
from emmetify.config.base_config import EmmetifierConfig
from emmetify.config.html_config import HtmlConfig


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

    def reverse_assert(self, expected_html: str, expected_abbr: str):
        """Assert that the reverse emmetified result is correct"""
        reversed_html = expand_emmet(expected_abbr)
        pretty_expected = BeautifulSoup(expected_html, "html.parser").prettify()
        pretty_reversed = BeautifulSoup(reversed_html, "html.parser").prettify()
        print(
            "\n\nExpected:\n",
            pretty_expected,
            "\n\nReversed:\n",
            pretty_reversed,
            "\n\n",
        )
        self.assertEqual(
            pretty_expected, pretty_reversed, "Reverse emmetified result is incorrect"
        )

    def emmetify_assert(
        self,
        emmetifier: Emmetifier,
        input_html: str,
        expected_abbr: str,
    ):
        """Assert that the emmetified result is correct and that the reverse is correct"""
        self.assertEqual(
            expected_abbr,
            emmetifier.emmetify(input_html)["result"],
            "Emmetified result is incorrect",
        )


class TestEmmetifierNoOptimization(BaseTestCase):
    def setUp(self):
        self.emmetifier = Emmetifier(config=EmmetifierConfig(debug=False, indent=False))

    def test_single_line_html(self):
        input_html = """
            <div id="main" class="container" data-test="ignore">
                Tytus Bomba
            </div>
        """
        expected_abbr = "div#main.container[data-test=ignore]{Tytus Bomba}"
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(input_html, expected_abbr)

    def test_multi_line_html(self):
        input_html = """
            <div id="main1" class="eren-container" data-test="ignore">Eren Yeager</div>
            <div id="main2" class="mikasa-container" data-test="ignore">Mikasa Ackerman</div>
        """
        expected_abbr = "div#main1.eren-container[data-test=ignore]{Eren Yeager}+div#main2.mikasa-container[data-test=ignore]{Mikasa Ackerman}"
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(input_html, expected_abbr)

    def test_simple_nested_structure(self):
        input_html = """
            <nav class="menu">
                <ul>
                    <li>
                        <a href="#home">Home</a>
                    </li>
                </ul>
            </nav>
        """
        expected_abbr = "nav.menu>ul>li>a[href=#home]{Home}"
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(input_html, expected_abbr)

    def test_multiple_nested_structures(self):
        input_html = """
            <nav class="menu">
                <ul>
                    <li id="no-children">
                    </li>
                    <li id="children">
                        <div id="2"></div>
                    </li>
                    <li><a href="#about">About</a></li>
                </ul>
                <div id="3"></div>
            </nav>
        """
        expected_abbr = "nav.menu>(ul>li#no-children+(li#children>div#2)+(li>a[href=#about]{About}))+div#3"
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(input_html, expected_abbr)

    def test_attributes_order(self):
        input_html = """
            <div id="main" class="container" data-test="ignore" data-test2="ignore2">
                Eren Yeager
            </div>
            <div id="main2" class="container" data-test="ignore" data-test2="ignore2">
                One Punch Man
            </div>
        """
        expected_abbr = "div#main.container[data-test=ignore data-test2=ignore2]{Eren Yeager}+div#main2.container[data-test=ignore data-test2=ignore2]{One Punch Man}"
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(input_html, expected_abbr)

    def test_attributes_with_spaces(self):
        input_html = """
            <div id="main" class="container" data-test="ignore" data-test2="ignore 2">
                Iron Man
            </div>
            <a href="https://example.com">Link</a>
        """
        expected_abbr = 'div#main.container[data-test=ignore data-test2="ignore 2"]{Iron Man}+a[href=https://example.com]{Link}'
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(input_html, expected_abbr)


class TestEmmetifierWithSkipTags(BaseTestCase):
    def setUp(self):
        self.emmetifier = Emmetifier(
            config=EmmetifierConfig(html=HtmlConfig(skip_tags=True))
        )

    def test_skip_tags_when_root_tag(self):
        input_html = """
            <link rel="stylesheet" href="style.css">
            <div id="main" class="container">
                Eren Yeager
            </div>
        """
        expected_abbr = "div#main.container{Eren Yeager}"
        expected_html = """
            <div id="main" class="container">
                Eren Yeager
            </div>
        """
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(expected_html, expected_abbr)

    def test_skip_tags_when_child_tag(self):
        input_html = """
            <div id="main" class="container">
                <link rel="stylesheet" href="style.css">
                <div id="child">
                    Eren Yeager
                </div>
            </div>
        """
        expected_abbr = "div#main.container>div#child{Eren Yeager}"
        expected_html = """
            <div id="main" class="container">
                <div id="child">
                    Eren Yeager
                </div>
            </div>
        """
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(expected_html, expected_abbr)

    def test_skip_tags_when_grandchild_tag(self):
        input_html = """
            <div id="main" class="container">
                <div id="child">
                    <div id="grandchild">
                        <link rel="stylesheet" href="style.css">
                        Eren Yeager
                    </div>
                </div>
            </div>
        """
        expected_abbr = "div#main.container>div#child>div#grandchild{Eren Yeager}"
        expected_html = """
            <div id="main" class="container">
                <div id="child">
                    <div id="grandchild">
                        Eren Yeager
                    </div>
                </div>
            </div>
        """
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(expected_html, expected_abbr)

    def test_skip_tags_multiple_cases(self):
        input_html = """
            <script src="script.js"></script>
            <div id="main" class="container">
                <link rel="stylesheet" href="style.css">
                <div id="child">
                    Eren Yeager
                </div>
            </div>
            <meta charset="UTF-8">
        """
        expected_abbr = "div#main.container>div#child{Eren Yeager}"
        expected_html = """
            <div id="main" class="container">
                <div id="child">
                    Eren Yeager
                </div>
            </div>
        """
        self.emmetify_assert(self.emmetifier, input_html, expected_abbr)
        self.reverse_assert(expected_html, expected_abbr)
