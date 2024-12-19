from unittest.mock import patch

from emmetify.config.base_config import EmmetifierConfig
from emmetify.converters.html_converter import HtmlConverter
from emmetify.parsers.html_parser import HtmlParser
from tests.utils import BaseEmmetTestCase


class TestHtmlConverterComplexCases(BaseEmmetTestCase):
    def setUp(self):
        self.config = EmmetifierConfig()
        self.config.html.simplify_classes = True
        self.config.html.simplify_links = True
        self.config.html.simplify_images = True
        self.config.html.skip_tags = False
        self.config.html.prioritize_attributes = False
        self.config.html.skip_empty_attributes = False
        self.config.indent = False

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_deep_nesting(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1", "token2", "token3", "token4"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="level1">
                <div class="level2">
                    <div class="level3">
                        <div class="level4">
                            Deep nested content
                        </div>
                    </div>
                </div>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = "div.token1>div.token2>div.token3>div.token4{Deep nested content}"
        self.assertEqual(expected_result, result["result"])

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_mixed_content(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = [
            "token1",
            "token2",
            "token3",
            "token4",
            "token5",
            "token6",
        ]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="container">
                <h1 class="title">Hello</h1>
                Some text
                <a href="https://example.com" class="link">Click</a>
                <img src="/test.jpg" class="image" alt="Test">
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)
        expected_result = "div.token1>h1.token2{Hello}+{Some text}+a.token3[href=token4]{Click}+img.token5[src=token6 alt=Test]"

        self.assertEqual(expected_result, result["result"])

        self.assertEqual("container", result["maps"]["classes"]["token1"])
        self.assertEqual("title", result["maps"]["classes"]["token2"])
        self.assertEqual("link", result["maps"]["classes"]["token3"])
        self.assertEqual("image", result["maps"]["classes"]["token5"])
        self.assertEqual("https://example.com", result["maps"]["links"]["token4"])
        self.assertEqual("/test.jpg", result["maps"]["images"]["token6"])

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_siblings_with_text(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="items">
                <span>First</span>
                <span>Second</span>
                <span>Third</span>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = "div.token1>span{First}+span{Second}+span{Third}"
        self.assertEqual(expected_result, result["result"])

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_empty_elements(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="wrapper">
                <br>
                <input type="text">
                <hr>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = "div.token1>br+input[type=text]+hr"
        self.assertEqual(expected_result, result["result"])

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_mixed_attributes(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="form" id="contact" data-test="value" style="display: none">
                <input type="text" required placeholder="Enter name">
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_result = 'div#contact.token1[data-test=value style="display: none"]>input[type=text required placeholder="Enter name"]'
        self.assertEqual(expected_result, result["result"])
