import unittest

from emmetify.utils.xpath import restore_links_in_xpath


class TestRestoreLinksInXPath(unittest.TestCase):
    def test_simple_replacement_v1(self):
        xpath = "//a[@href='https://example.com']"
        # xpath = "//a[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//a[@href='https://example.com']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_simple_replacement_v2(self):
        xpath = "/a[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "/a[@href='https://example.com']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_no_replacement_href_not_in_replace_map(self):
        xpath = "//a[@href='john']"
        replace_map = {"jane": "https://example.com"}
        expected = "//a[@href='john']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_in_other_tag_not_replaced(self):
        xpath = "//div[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//div[@href='john']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_mixed_tags_and_attributes(self):
        xpath = "//a[@href='john']//img[@src='john']//span[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//a[@href='https://example.com']//img[@src='john']//span[@href='john']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_empty_xpath(self):
        xpath = ""
        replace_map = {"john": "https://example.com"}
        expected = ""
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_different_quotes(self):
        xpath = '//a[@href="john"]'
        replace_map = {"john": "https://example.com"}
        expected = '//a[@href="https://example.com"]'
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_contains_function(self):
        xpath = "//a[contains(@href,'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//a[contains(@href,'https://example.com')]"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_nested_a_tags(self):
        xpath = "//div//a[@href='john']//a[@href='doe']"
        replace_map = {"john": "https://example.com", "doe": "https://example.org"}
        expected = "//div//a[@href='https://example.com']//a[@href='https://example.org']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_multiple_predicates(self):
        xpath = "//a[@class='link'][@href='john'][@id='main']"
        replace_map = {"john": "https://example.com"}
        expected = "//a[@class='link'][@href='https://example.com'][@id='main']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_starts_with_function(self):
        xpath = "//a[starts-with(@href,'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//a[starts-with(@href,'https://example.com')]"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_normalize_space_function(self):
        xpath = "//a[normalize-space(@href)='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//a[normalize-space(@href)='https://example.com']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_ends_with_and_normalize_space_functions(self):
        xpath = "//a[ends-with(normalize-space(@href),'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//a[ends-with(normalize-space(@href),'https://example.com')]"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_multiple_predicates_and_functions(self):
        xpath = "//a[@class='link' and contains(@href,'john')]"
        replace_map = {"john": "https://example.com"}
        expected = "//a[@class='link' and contains(@href,'https://example.com')]"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_complex_xpath_expression(self):
        xpath = "//div//a[@href='john' and @data-id='123']//span[text()='Click here']"
        replace_map = {"john": "https://example.com"}
        expected = (
            "//div//a[@href='https://example.com' and @data-id='123']//span[text()='Click here']"
        )
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_in_namespaced_tag_not_replaced(self):
        xpath = "//my:a[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//my:a[@href='john']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_in_other_tag_with_a_in_name(self):
        xpath = "//span[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//span[@href='john']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_axis_notation(self):
        xpath = "//child::a[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//child::a[@href='https://example.com']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_axis_notation_and_namespace(self):
        xpath = "//child::my:a[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//child::my:a[@href='john']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_quotes_inside_value(self):
        xpath = "//a[@href=\"Jo'hn's site\"]"
        replace_map = {"Jo'hn's site": "https://example.com"}
        expected = '//a[@href="https://example.com"]'
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_special_characters(self):
        xpath = "//a[@href='john & jane?']"
        replace_map = {"john & jane?": "https://example.com"}
        expected = "//a[@href='https://example.com']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_escaped_quotes(self):
        xpath = "//a[@href='john\\'s site']"
        replace_map = {"john's site": "https://example.com"}
        expected = (
            "//a[@href='john\\'s site']"  # Should not replace because the value doesn't match
        )
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_non_string_value(self):
        xpath = "//a[@href='123']"
        replace_map = {123: "https://example.com"}  # Key is integer, should not match
        expected = "//a[@href='123']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_function_inside_predicate(self):
        xpath = "//a[@href=concat('john','doe')]"
        replace_map = {"johndoe": "https://example.com"}
        expected = "//a[@href=concat('john','doe')]"  # Should not replace, value is an expression
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_variable_in_predicate(self):
        xpath = "//a[@href=$john]"
        replace_map = {"$john": "https://example.com"}
        expected = "//a[@href=$john]"  # Should not replace, value is a variable reference
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_multiple_attributes_in_predicate(self):
        xpath = "//a[@href='john' and @title='Home']"
        replace_map = {"john": "https://example.com"}
        expected = "//a[@href='https://example.com' and @title='Home']"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_comment_in_predicate(self):
        xpath = "//a[@href='john'/*comment*/]"
        replace_map = {"john": "https://example.com"}
        expected = "//a[@href='https://example.com'/*comment*/]"
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_namespace_prefix_matching_a(self):
        xpath = "//a:a[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//a:a[@href='john']"  # Should not replace because 'a:a' != 'a'
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_href_with_case_sensitive_tag_name(self):
        xpath = "//A[@href='john']"
        replace_map = {"john": "https://example.com"}
        expected = "//A[@href='john']"  # Tag name is 'A', not 'a'
        result = restore_links_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)
