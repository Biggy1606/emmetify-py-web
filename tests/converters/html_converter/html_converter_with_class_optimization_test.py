from unittest.mock import Mock, patch

from bs4 import Tag

from emmetify.config.base_config import EmmetifierConfig
from emmetify.converters.html_converter import HtmlConverter
from emmetify.parsers.html_parser import HtmlParser
from tests.utils import BaseEmmetTestCase


class TestHtmlConverterWithClassOptimization(BaseEmmetTestCase):
    def setUp(self):
        self.config = EmmetifierConfig()
        self.config.html.simplify_classes = True
        self.config.html.simplify_absolute_links = False
        self.config.html.simplify_relative_links = False
        self.config.html.simplify_images = False
        self.config.html.skip_tags = False
        self.config.html.prioritize_attributes = False
        self.config.html.skip_empty_attributes = False
        self.config.indent = False

    def _create_mock_tag(self, name: str, attrs: dict) -> Mock:
        mock_tag = Mock(spec=Tag)
        mock_tag.name = name
        mock_tag.attrs = attrs
        return mock_tag

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_class_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1", "token2"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="test-class another-class">
                Eren Yeager
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_class_map = {"token1": "test-class another-class"}
        expected_result = "div.token1{Eren Yeager}"
        self.assertEqual(expected_class_map, result.maps.classes)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_multiple_nodes_class_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1", "token2"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div class="parent-class">
                <div class="child-class">
                    Eren Yeager
                </div>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_class_map = {"token1": "parent-class", "token2": "child-class"}
        expected_result = "div.token1>div.token2{Eren Yeager}"
        self.assertEqual(expected_class_map, result.maps.classes)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_reused_classes_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        converter = HtmlConverter(self.config)
        parser = HtmlParser(self.config)

        input_html = """
            <div class="same-class">
                <div class="same-class">
                    Eren Yeager
                </div>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_class_map = {"token1": "same-class"}
        expected_result = "div.token1>div.token1{Eren Yeager}"
        self.assertEqual(expected_class_map, result.maps.classes)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_nested_nodes_with_multiple_classes(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1", "token2", "token3"]

        converter = HtmlConverter(self.config)
        parser = HtmlParser(self.config)

        input_html = """
            <div class="parent-class wrapper">
                <div class="child-class">
                </div>
                <div class="wrapper">
                    Eren Yeager
                </div>
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_class_map = {
            "token1": "parent-class wrapper",
            "token2": "child-class",
            "token3": "wrapper",
        }
        expected_result = "div.token1>div.token2+div.token3{Eren Yeager}"

        self.assertEqual(expected_class_map, result.maps.classes)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_without_text_nodes(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        converter = HtmlConverter(self.config)
        parser = HtmlParser(self.config)

        input_html = """
            <div class="container"></div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_class_map = {"token1": "container"}
        expected_result = "div.token1"
        self.assertEqual(expected_class_map, result.maps.classes)
        self.assertEqual(expected_result, result.result)
