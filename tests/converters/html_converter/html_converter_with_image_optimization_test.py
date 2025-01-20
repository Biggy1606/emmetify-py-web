from unittest.mock import patch

from emmetify.config.base_config import EmmetifierConfig
from emmetify.converters.html_converter import HtmlConverter
from emmetify.parsers.html_parser import HtmlParser
from tests.utils import BaseEmmetTestCase


class TestHtmlConverterWithImageOptimization(BaseEmmetTestCase):
    def setUp(self):
        self.config = EmmetifierConfig()
        self.config.html.simplify_classes = False
        self.config.html.simplify_links = False
        self.config.html.simplify_images = True
        self.config.html.skip_tags = False
        self.config.html.prioritize_attributes = False
        self.config.html.skip_empty_attributes = False
        self.config.indent = False

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_image_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <img src="/images/test.jpg" alt="Test image">
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_images_map = {"token1": "/images/test.jpg"}
        expected_result = 'img[src=token1 alt="Test image"]'
        self.assertEqual(expected_images_map, result.maps.images)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_multiple_images_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1", "token2"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                <img src="/images/first.jpg" alt="First image">
                <img src="/images/second.jpg" alt="Second image">
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_images_map = {
            "token1": "/images/first.jpg",
            "token2": "/images/second.jpg",
        }
        expected_result = 'div>img[src=token1 alt="First image"]+img[src=token2 alt="Second image"]'
        self.assertEqual(expected_images_map, result.maps.images)
        self.assertEqual(expected_result, result.result)

    @patch("emmetify.converters.html_converter.SingleTokenNames")
    def test_reused_images_mapping(self, mock_single_token_names):
        mock_instance = mock_single_token_names.return_value
        mock_instance.get_name.side_effect = ["token1"]

        parser = HtmlParser(self.config)
        converter = HtmlConverter(self.config)

        input_html = """
            <div>
                <img src="/images/test.jpg" alt="First">
                <img src="/images/test.jpg" alt="Second">
            </div>
        """
        node_pool = parser.parse(input_html)
        result = converter.convert(node_pool)

        expected_images_map = {"token1": "/images/test.jpg"}
        expected_result = "div>img[src=token1 alt=First]+img[src=token1 alt=Second]"
        self.assertEqual(expected_images_map, result.maps.images)
        self.assertEqual(expected_result, result.result)
