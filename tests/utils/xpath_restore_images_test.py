import unittest

from emmetify.utils.xpath import restore_images_in_xpath


class TestRestoreImagesInXPath(unittest.TestCase):
    def test_simple_replacement_v1(self):
        xpath = "//img[@src='https://example.com']"
        replace_map = {"john": "https://example.com"}
        expected = "//img[@src='https://example.com']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_simple_replacement_v2(self):
        xpath = "/img[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "/img[@src='https://example.com']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_no_replacement_src_not_in_replace_map(self):
        xpath = "//img[@src='john']"
        replace_map = {"jane": "https://example.com"}
        expected = "//img[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_in_other_tag_not_replaced(self):
        xpath = "//div[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//div[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_mixed_tags_and_attributes(self):
        xpath = "//img[@src='john']//a[@href='john']//span[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//img[@src='https://example.com']//a[@href='john']//span[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_empty_xpath(self):
        xpath = ""
        replace_map = {"john": "https://example.com"}
        expected = ""
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_different_quotes(self):
        xpath = '//img[@src="john"]'
        replace_map = {"john": "https://example.com"}
        expected = '//img[@src="https://example.com"]'
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_contains_function(self):
        xpath = "//img[contains(@src,'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//img[contains(@src,'https://example.com')]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_nested_img_tags(self):
        xpath = "//div//img[@src='john']//img[@src='doe']"
        replace_map = {"john": "https://example.com", "doe": "https://example.org"}
        expected = "//div//img[@src='https://example.com']//img[@src='https://example.org']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_multiple_predicates(self):
        xpath = "//img[@class='image'][@src='john'][@id='main']"
        replace_map = {"john": "https://example.com"}
        expected = "//img[@class='image'][@src='https://example.com'][@id='main']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_starts_with_function(self):
        xpath = "//img[starts-with(@src,'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//img[starts-with(@src,'https://example.com')]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_normalize_space_function(self):
        xpath = "//img[normalize-space(@src)='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//img[normalize-space(@src)='https://example.com']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_ends_with_and_normalize_space_functions(self):
        xpath = "//img[ends-with(normalize-space(@src),'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//img[ends-with(normalize-space(@src),'https://example.com')]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_multiple_predicates_and_functions(self):
        xpath = "//img[@class='image' and contains(@src,'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//img[@class='image' and contains(@src,'https://example.com')]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_complex_xpath_expression(self):
        xpath = "//div//img[@src='john' and @data-id='123']//span[text()='Click here']"
        replace_map = {"john": "https://example.com"}
        expected = (
            "//div//img[@src='https://example.com' and @data-id='123']//span[text()='Click here']"
        )
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_in_namespaced_tag_not_replaced(self):
        xpath = "//my:img[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//my:img[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_in_other_tag_with_img_in_name(self):
        xpath = "//span[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//span[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_axis_notation(self):
        xpath = "//child::img[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//child::img[@src='https://example.com']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_axis_notation_and_namespace(self):
        xpath = "//child::my:img[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//child::my:img[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_quotes_inside_value(self):
        xpath = "//img[@src=\"Jo'hn's image\"]"
        replace_map = {"Jo'hn's image": "https://example.com"}
        expected = '//img[@src="https://example.com"]'
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_special_characters(self):
        xpath = "//img[@src='john & jane?']"
        replace_map = {"john & jane?": "https://example.com"}
        expected = "//img[@src='https://example.com']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_escaped_quotes(self):
        xpath = "//img[@src='john\\'s image']"
        replace_map = {"john's image": "https://example.com"}
        expected = "//img[@src='john\\'s image']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_non_string_value(self):
        xpath = "//img[@src='123']"
        replace_map = {123: "https://example.com"}
        expected = "//img[@src='123']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_function_inside_predicate(self):
        xpath = "//img[@src=concat('john','doe')]"
        replace_map = {"johndoe": "https://example.com"}
        expected = "//img[@src=concat('john','doe')]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_variable_in_predicate(self):
        xpath = "//img[@src=$john]"
        replace_map = {"$john": "https://example.com"}
        expected = "//img[@src=$john]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_multiple_attributes_in_predicate(self):
        xpath = "//img[@src='john' and @title='Home']"
        replace_map = {"john": "https://example.com"}
        expected = "//img[@src='https://example.com' and @title='Home']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_comment_in_predicate(self):
        xpath = "//img[@src='john'/*comment*/]"
        replace_map = {"john": "https://example.com"}
        expected = "//img[@src='https://example.com'/*comment*/]"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_namespace_prefix_matching_img(self):
        xpath = "//img:img[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//img:img[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_src_with_case_sensitive_tag_name(self):
        xpath = "//IMG[@src='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//IMG[@src='john']"
        result = restore_images_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)
