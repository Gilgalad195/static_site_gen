import unittest

from htmlnode import HTMLNode

class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_1(self):
        node = HTMLNode("a", "hello to the whole world", ["child"], {"href": "www.boot.dev"})
        #print(node.props_tohtml())
        self.assertEqual(node.props_tohtml(), ' href="www.boot.dev"')

    def test_props_to_html_2(self):
        node = HTMLNode("a", "hello to the whole world", ["child"], {"href": "www.boot.dev", "target": "_blank"})
        #print(node.props_tohtml())
        self.assertEqual(node.props_tohtml(), ' href="www.boot.dev" target="_blank"')

    def test_props_to_html_3(self):
        node = HTMLNode("a", "hello to the whole world")
        #print(node.props_tohtml())
        self.assertEqual(node.props_tohtml(), '')

if __name__ == "__main__":
    unittest.main()