from unittest.mock import patch

from emmetify.config.base_config import EmmetifierConfig
from emmetify.converters.html_converter import HtmlConverter
from emmetify.parsers.html_parser import HtmlParser
from tests.utils import BaseEmmetTestCase


class TestHtmlConverterWithLinkOptimization(BaseEmmetTestCase):
    def setUp(self):
        self.config = EmmetifierConfig()
        self.config.html.simplify_classes = False
        self.config.html.simplify_links = True
        self.config.html.simplify_images = False
        self.config.html.skip_tags = False
        self.config.html.prioritize_attributes = False
        self.config.html.skip_empty_attributes = False
        self.config.indent = False

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_link_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <a href="https://example.com">Click me</a>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_links_map = {"token1": "https://example.com"}
        expected_result = "a[href=token1]{Click me}"
        self.assertEqual(expected_links_map, result.maps.links)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_multiple_links_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1", "token2"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                <a href="https://example.com">First link</a>
                <a href="https://another.com">Second link</a>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_links_map = {
            "token1": "https://example.com",
            "token2": "https://another.com",
        }
        expected_result = "div>a[href=token1]{First link}+a[href=token2]{Second link}"
        self.assertEqual(expected_links_map, result.maps.links)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_reused_links_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                <a href="https://example.com">First link</a>
                <a href="https://example.com">Same link</a>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_links_map = {"token1": "https://example.com"}
        expected_result = "div>a[href=token1]{First link}+a[href=token1]{Same link}"
        self.assertEqual(expected_links_map, result.maps.links)
        self.assertEqual(expected_result, result.result)
