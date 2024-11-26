import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html(self):
        node = HTMLNode(
            None, None, None, {
                "href": "https://www.google.com", 
                "target": "_blank"
            }
        )
        self.assertEqual(
            node.props_to_html(), 
            " href=\"https://www.google.com\" target=\"_blank\""
        )

    def test_repr(self):
        node = HTMLNode(
            "<p>", "Hello World", None, {
                "href": "https://www.google.com", "target": "_blank"
            }
        )
        self.assertEqual(
            node.__repr__(),
            "<p>\nHello World\nNone\n{\'href\': \'https://www.google.com\', \'target\': \'_blank\'}"
        )

if __name__ == "__main__":
    unittest.main()