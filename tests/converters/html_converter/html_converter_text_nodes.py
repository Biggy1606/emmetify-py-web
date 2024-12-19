import unittest

from emmetify.config.base_config import EmmetifierConfig
from emmetify.converters.html_converter import HtmlConverter
from emmetify.parsers.html_parser import HtmlParser
from tests.utils import BaseEmmetTestCase


class TestHtmlConverterTextNodes(BaseEmmetTestCase):
    def setUp(self):
        self.config = EmmetifierConfig()
        self.config.html.simplify_classes = False
        self.config.html.simplify_links = False
        self.config.html.simplify_images = False
        self.config.indent = False

    def test_text_node_with_special_characters(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                Text with * asterisk, $ dollar, { curly }, [ square ], + plus
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = (
            r"div{Text with \* asterisk, \$ dollar, { curly }, [ square ], + plus}"
        )
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_node_when_it_is_the_only_child(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = "<div>Text</div>"
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)
        expected_result = "div{Text}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_node_when_it_is_not_the_on_the_beginning_of_the_tag(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                <span>Text 1</span>
                Not on the beginning
                <span>Text 2</span>
            </div>
        """

        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)
        expected_result = "div>span{Text 1}+{Not on the beginning}+span{Text 2}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_multiple_text_nodes_between_elements(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                First text
                <span>Middle</span>
                Second text
                <span>End</span>
                Last text
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = (
            "div{First text}>span{Middle}+{Second text}+span{End}+{Last text}"
        )
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_mixed_text_and_elements_deep_nesting(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                Root text
                <div>
                    Level 1 text
                    <div>
                        Level 2 text
                        <span>Span text</span>
                        After span text
                    </div>
                    After level 2 text
                </div>
                Final text
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = "div{Root text}>div{Level 1 text}>div{Level 2 text}>span{Span text}+{After span text}+{After level 2 text}+{Final text}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_nodes_with_whitespace(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                   Text with    multiple    spaces   
                <span>    Indented     text    </span>
                   More    spaces   
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        # Whitespace should be normalized but preserved
        expected_result = (
            "div{Text with multiple spaces}>span{Indented text}+{More spaces}"
        )
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_nodes_with_html_entities(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                Text with &amp; ampersand &lt; less than &gt; greater than &quot; quote
                <span>&copy; copyright &reg; registered</span>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = 'div{Text with & ampersand < less than > greater than " quote}>span{© copyright ® registered}'
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_nodes_in_list_structures(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <ul>
                Text before list
                <li>First item</li>
                Between items
                <li>Second item</li>
                After items
            </ul>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = "ul{Text before list}>li{First item}+{Between items}+li{Second item}+{After items}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_empty_and_whitespace_text_nodes(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                
                <span>Content</span>
                
                <span>More</span>
                
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        # Empty text nodes should be ignored
        expected_result = "div>span{Content}+span{More}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_nodes_with_newlines(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                First line
                Second line
                <span>Third
                line</span>
                Fourth
                line
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        # Newlines should be preserved as spaces
        expected_result = "div{First line Second line}>span{Third line}+{Fourth line}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_nodes_with_unicode(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                Unicode: 你好 مرحبا Привет
                <span>Emojis: 👋 🌟 🎉</span>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = "div{Unicode: 你好 مرحبا Привет}>span{Emojis: 👋 🌟 🎉}"
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_nodes_with_math_symbols(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                Math: 2 × 3 ÷ 4 ≠ 5 ± 6 ≤ 7 ≥ 8 ≈ 9
                <span>More: ∑(x²) = ∞</span>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = (
            "div{Math: 2 × 3 ÷ 4 ≠ 5 ± 6 ≤ 7 ≥ 8 ≈ 9}>span{More: ∑(x²) = ∞}"
        )
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_nested_elements_with_text(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                Outer start
                <div>
                    Inner text
                    <span>Span text</span>
                    More inner
                </div>
                Outer end
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = (
            "div{Outer start}>div{Inner text}>span{Span text}+{More inner}+{Outer end}"
        )
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)

    def test_text_with_inline_elements(self):
        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <p>
                Start text
                <strong>bold</strong>
                middle text
                <em>italic</em>
                end text
            </p>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = (
            "p{Start text}>strong{bold}+{middle text}+em{italic}+{end text}"
        )
        self.assertEqual(expected_result, result["result"])
        self.emmet_reverse_assert(input_html, result)
