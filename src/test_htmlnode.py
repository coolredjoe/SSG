import unittest

from htmlnode import HTMLNode, LeafNode


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
    
    def test_leaf_nodes(self):
        node1 = LeafNode("p", "This is a paragraph of text.")
        node2 = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        node3 = LeafNode(None, "Click me!", {"href": "https://www.google.com"})
        self.assertEqual(node1.to_html(), "<p>This is a paragraph of text.</p>")
        self.assertEqual(node2.to_html(), "<a href=\"https://www.google.com\">Click me!</a>")
        self.assertEqual(node3.to_html(), "Click me!")        

if __name__ == "__main__":
    unittest.main()