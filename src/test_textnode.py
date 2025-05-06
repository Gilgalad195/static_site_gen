import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_ne_1(self):
        node = TextNode("This might be a text node", TextType.ITALIC)
        node2 = TextNode("This is definitely a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_ne_2(self):
        node = TextNode("sample text string", TextType.ITALIC, "https://www.boot.dev")
        node2 = TextNode("sample text string", TextType.ITALIC, "https://www.boot.dev")
        self.assertEqual(node, node2)

    def test_ne_3(self):
        node = TextNode("sample text string", TextType.ITALIC, "https://www.")
        node2 = TextNode("sample text string", TextType.ITALIC, "https://www.boot.dev")
        self.assertNotEqual(node, node2) 

    def test_ne_4(self):
        node = TextNode("sample text string", TextType.ITALIC,)
        node2 = TextNode("sample text string", TextType.ITALIC, "https://www.boot.dev")
        self.assertNotEqual(node, node2)          


if __name__ == "__main__":
    unittest.main()