import unittest
from scraper import (
    add_domain_if_required,
    is_external_resource,
    generate_word_freq_dict,
)
from attrdict import AttrDict
from collections import Counter


class TestScraper(unittest.TestCase):
    def setUp(self):
        self.url = "https://www.some-random-url.es/1651651fhjksd.dfhudhiosuf.w"

    def test_is_external_resource(self):
        mock_tag = AttrDict(
            {
                "name": "foo",
                "src": "https://static.files.co.uk/orbi/9dc2b29require.min.js",
            }
        )
        self.assertTrue(is_external_resource(mock_tag, self.url))

        mock_tag = AttrDict(
            {
                "name": "foo",
                "href": "https://www.some-random-url.es/orbi/6456.lkl/878.img",
            }
        )
        self.assertFalse(is_external_resource(mock_tag, self.url))

        mock_tag = AttrDict({"name": "foo"})
        self.assertFalse(is_external_resource(mock_tag, self.url))

        mock_tag = AttrDict({"src": None, "name": "foo"})
        self.assertFalse(is_external_resource(mock_tag, self.url))

        mock_tag = AttrDict({"href": "", "name": "foo"})
        self.assertFalse(is_external_resource(mock_tag, self.url))

    def test_is_external_resource_with_anchor(self):
        mock_tag = AttrDict(
            {
                "name": "a",
                "href": "https://static.files.co.uk/orbi/9dc2b29reque.mi",
            }
        )
        self.assertFalse(is_external_resource(mock_tag, self.url))

        mock_tag = AttrDict(
            {
                "name": "a",
                "href": "https://www.some-random-url.es/orbi/9dc2b29reque.mi",
            }
        )
        self.assertFalse(is_external_resource(mock_tag, self.url))

    def test_generate_word_freq_dict(self):
        test_string = ' 25654   dog \b\b\n     house \\ "\t dog 5g cat    \f '
        expected_counter = Counter({"dog": 2, "house": 1, "cat": 1})
        self.assertEqual(
            generate_word_freq_dict(test_string), expected_counter
        )

    def test_add_domain_if_required(self):
        href = "/contacts/index.html"
        expected_address = "www.some-random-url.es/contacts/index.html"
        self.assertEqual(
            add_domain_if_required(href, self.url), expected_address
        )

        href = "www.some-random-url.es/contacts/index.html"
        expected_address = "www.some-random-url.es/contacts/index.html"
        self.assertEqual(
            add_domain_if_required(href, self.url), expected_address
        )
