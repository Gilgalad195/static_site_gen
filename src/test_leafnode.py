import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

class TestLeafNode(unittest.TestCase):
    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!")
        self.assertEqual(node.to_html(), "<p>Hello, world!</p>")

    def test_leaf_to_html_li(self):
        node = LeafNode("li", "Hello, world!")
        self.assertEqual(node.to_html(), "<li>Hello, world!</li>")

    def test_leaf_to_html_ul(self):
        node = LeafNode("ul", "Hello, world!", {"href": "www.boot.dev"})
        self.assertEqual(node.to_html(), '<ul href="www.boot.dev">Hello, world!</ul>')

    def test_leaf_to_html_blank_tag(self):
        node = LeafNode(None, "Hello, world!")
        self.assertEqual(node.to_html(), "Hello, world!")

    def test_leaf_to_html_blank_value(self):
        node = LeafNode("p", None)
        with self.assertRaises(ValueError):
            node.to_html()
            

if __name__ == "__main__":
    unittest.main()