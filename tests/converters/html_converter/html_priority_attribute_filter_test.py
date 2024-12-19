import unittest

from emmetify.config.html_config import HtmlAttributesPriority
from emmetify.converters.html_converter import HtmlPriorityAttributeFilter


class TestHtmlPriorityAttributeFilter(unittest.TestCase):
    def setUp(self):
        self.priority_config = HtmlAttributesPriority(
            primary_attrs={"id", "class"},
            secondary_attrs={"href", "src"},
            ignore_attrs={"style"},
        )
        self.filter = HtmlPriorityAttributeFilter(self.priority_config)

    def test_filter_attributes_with_primary(self):
        attrs = {
            "id": "main",
            "class": "container",
            "style": "display: none",
            "data-test": "value",
            "onclick": "handleClick()",
        }
        expected = {"id": "main", "class": "container"}
        result = self.filter.filter_attributes(attrs)
        self.assertEqual(result, expected)

    def test_filter_attributes_with_secondary(self):
        attrs = {"href": "/home", "src": "image.jpg", "style": "display: none"}
        expected = {"href": "/home", "src": "image.jpg"}
        result = self.filter.filter_attributes(attrs)
        self.assertEqual(expected, result)
