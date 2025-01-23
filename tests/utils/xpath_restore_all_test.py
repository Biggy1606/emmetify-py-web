import unittest
from dataclasses import dataclass

from emmetify.utils.xpath import restore_xpath_from_converter_maps


@dataclass
class HtmlConverterMaps:
    classes: dict[str, str]
    links: dict[str, str]
    images: dict[str, str]


class TestRestoreXPathFromConverterMaps(unittest.TestCase):
    def test_restore_all_attributes(self):
        xpath = "//div[@class='old-class']//a[@href='old-link']//img[@src='old-image']"
        maps = HtmlConverterMaps(
            classes={"old-class": "new-class"},
            links={"old-link": "https://example.com"},
            images={"old-image": "https://example.com/image.jpg"},
        )
        expected = "//div[@class='new-class']//a[@href='https://example.com']//img[@src='https://example.com/image.jpg']"
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)

    def test_restore_with_mixed_functions(self):
        xpath = "//div[contains(@class,'old-class')]//a[ends-with(@href,'old-link')]//img[starts-with(@src,'old-image')]"
        maps = HtmlConverterMaps(
            classes={"old-class": "new-class"},
            links={"old-link": "https://example.com"},
            images={"old-image": "https://example.com/image.jpg"},
        )
        expected = "//div[contains(@class,'new-class')]//a[ends-with(@href,'https://example.com')]//img[starts-with(@src,'https://example.com/image.jpg')]"
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)

    def test_restore_with_normalize_space(self):
        xpath = """//div[normalize-space(@class)='old-class']//
                   a[ends-with(normalize-space(@href),'old-link')]//
                   img[contains(normalize-space(@src),'old-image')]"""
        maps = HtmlConverterMaps(
            classes={"old-class": "new-class"},
            links={"old-link": "https://example.com"},
            images={"old-image": "https://example.com/image.jpg"},
        )
        expected = """//div[normalize-space(@class)='new-class']//
                   a[ends-with(normalize-space(@href),'https://example.com')]//
                   img[contains(normalize-space(@src),'https://example.com/image.jpg')]"""
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)

    def test_restore_with_empty_maps(self):
        xpath = "//div[@class='old-class']//a[@href='old-link']//img[@src='old-image']"
        maps = HtmlConverterMaps(classes={}, links={}, images={})
        expected = xpath
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)

    def test_restore_with_mixed_attributes_in_single_tag(self):
        # href and class in img tag - both should be replaced
        xpath = "//img[@class='old-class' and @src='old-image' and @href='old-link']"
        maps = HtmlConverterMaps(
            classes={"old-class": "new-class"},
            links={"old-link": "https://example.com"},
            images={"old-image": "https://example.com/image.jpg"},
        )
        expected = "//img[@class='new-class' and @src='https://example.com/image.jpg' and @href='old-link']"
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)

        # href and class in div tag - only class should be replaced
        xpath = "//div[@class='old-class' and @href='old-link']"
        expected = "//div[@class='new-class' and @href='old-link']"
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)
        xpath = """//div[@class='old-class' and @id='header']//
                   a[@href='old-link' or contains(@title,'click')]//
                   img[@src='old-image' and position()=1]"""
        maps = HtmlConverterMaps(
            classes={"old-class": "new-class"},
            links={"old-link": "https://example.com"},
            images={"old-image": "https://example.com/image.jpg"},
        )
        expected = """//div[@class='new-class' and @id='header']//
                   a[@href='https://example.com' or contains(@title,'click')]//
                   img[@src='https://example.com/image.jpg' and position()=1]"""
        result = restore_xpath_from_converter_maps(xpath, maps)
        self.assertEqual(result, expected)
