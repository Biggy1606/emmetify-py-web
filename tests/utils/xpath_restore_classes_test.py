import unittest

from emmetify.utils.xpath import restore_classes_in_xpath


class TestRestoreClassesInXPath(unittest.TestCase):
    def test_simple_replacement_v1(self):
        xpath = "//*[@class='example-class']"
        replace_map = {"john": "example-class"}
        expected = "//*[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_simple_replacement_v2(self):
        xpath = "//*[@class='john']"
        replace_map = {"john": "example-class"}
        expected = "//*[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_no_replacement_class_not_in_replace_map(self):
        xpath = "//*[@class='john']"
        replace_map = {"jane": "example-class"}
        expected = "//*[@class='john']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_mixed_tags_and_attributes(self):
        xpath = "//div[@class='john']//img[@src='john']//span[@class='john']"
        replace_map = {"john": "example-class"}
        expected = "//div[@class='example-class']//img[@src='john']//span[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_empty_xpath(self):
        xpath = ""
        replace_map = {"john": "example-class"}
        expected = ""
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_different_quotes(self):
        xpath = '//*[@class="john"]'
        replace_map = {"john": "example-class"}
        expected = '//*[@class="example-class"]'
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_contains_function(self):
        xpath = "//*[contains(@class,'john')]"
        replace_map = {"john": "example-class"}
        expected = "//*[contains(@class,'example-class')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_nested_elements(self):
        xpath = "//div//span[@class='john']//p[@class='doe']"
        replace_map = {"john": "primary", "doe": "secondary"}
        expected = "//div//span[@class='primary']//p[@class='secondary']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_multiple_predicates(self):
        xpath = "//*[@class='john'][@id='main'][@data-test='true']"
        replace_map = {"john": "example-class"}
        expected = "//*[@class='example-class'][@id='main'][@data-test='true']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_starts_with_function(self):
        xpath = "//*[starts-with(@class,'john')]"
        replace_map = {"john": "example-class"}
        expected = "//*[starts-with(@class,'example-class')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_normalize_space_function(self):
        xpath = "//*[normalize-space(@class)='john']"
        replace_map = {"john": "example-class"}
        expected = "//*[normalize-space(@class)='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_ends_with_and_normalize_space_functions(self):
        xpath = "//*[ends-with(normalize-space(@class),'john')]"
        replace_map = {"john": "example-class"}
        expected = "//*[ends-with(normalize-space(@class),'example-class')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_multiple_predicates_and_functions(self):
        xpath = "//*[@id='test' and contains(@class,'john')]"
        replace_map = {"john": "example-class"}
        expected = "//*[@id='test' and contains(@class,'example-class')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_multiple_predicates_and_functions_with_space(self):
        xpath = "//*[@id='test' and contains(@class, 'john')]"
        replace_map = {"john": "example-class"}
        expected = "//*[@id='test' and contains(@class, 'example-class')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_complex_xpath_expression(self):
        xpath = "//div//*[@class='john' and @data-id='123']//span[text()='Click here']"
        replace_map = {"john": "example-class"}
        expected = "//div//*[@class='example-class' and @data-id='123']//span[text()='Click here']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_in_namespaced_tag(self):
        xpath = "//my:div[@class='john']"
        replace_map = {"john": "example-class"}
        expected = "//my:div[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_axis_notation(self):
        xpath = "//child::*[@class='john']"
        replace_map = {"john": "example-class"}
        expected = "//child::*[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_axis_notation_and_namespace(self):
        xpath = "//child::my:*[@class='john']"
        replace_map = {"john": "example-class"}
        expected = "//child::my:*[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_quotes_inside_value(self):
        xpath = "//*[@class=\"Jo'hn's class\"]"
        replace_map = {"Jo'hn's class": "example-class"}
        expected = '//*[@class="example-class"]'
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_special_characters(self):
        xpath = "//*[@class='john & jane?']"
        replace_map = {"john & jane?": "example-class"}
        expected = "//*[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_escaped_quotes(self):
        xpath = "//*[@class='john\\'s class']"
        replace_map = {"john's class": "example-class"}
        expected = "//*[@class='john\\'s class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_non_string_value(self):
        xpath = "//*[@class='123']"
        replace_map = {123: "example-class"}
        expected = "//*[@class='123']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_function_inside_predicate(self):
        xpath = "//*[@class=concat('john','doe')]"
        replace_map = {"johndoe": "example-class"}
        expected = "//*[@class=concat('john','doe')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_function_inside_predicate_with_space(self):
        xpath = "//*[@class=concat('john', 'doe')]"
        replace_map = {"johndoe": "example-class"}
        expected = "//*[@class=concat('john', 'doe')]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_variable_in_predicate(self):
        xpath = "//*[@class=$john]"
        replace_map = {"$john": "example-class"}
        expected = "//*[@class=$john]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_multiple_attributes_in_predicate(self):
        xpath = "//*[@class='john' and @title='Main']"
        replace_map = {"john": "example-class"}
        expected = "//*[@class='example-class' and @title='Main']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_comment_in_predicate(self):
        xpath = "//*[@class='john'/*comment*/]"
        replace_map = {"john": "example-class"}
        expected = "//*[@class='example-class'/*comment*/]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_double_slash_and_index(self):
        xpath = "//footer//div[contains(@class, 'omi')]/text()[2]"
        replace_map = {"omi": "example-class"}
        expected = "//footer//div[contains(@class, 'example-class')]/text()[2]"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)

    def test_class_with_case_sensitive_tag_name(self):
        xpath = "//DIV[@class='john']"
        replace_map = {"john": "example-class"}
        expected = "//DIV[@class='example-class']"
        result = restore_classes_in_xpath(xpath, replace_map)
        self.assertEqual(result, expected)
