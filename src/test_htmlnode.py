import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode
from textnode import TextNode, TextType
from node_conversion import *
from inline_markdown import *

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

class TestParentNode(unittest.TestCase):
    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(),
            "<div><span><b>grandchild</b></span></div>",
        )

    def test_to_html_with_greatgrand(self):
        greatgrand_node = LeafNode("a", "greatgrand")
        grandchild_node = ParentNode("p", [greatgrand_node], {"href": "www.boot.dev"})
        child_node = ParentNode("h1", [grandchild_node])
        parent_node = ParentNode("span", [child_node])
        self.assertEqual(parent_node.to_html(), '<span><h1><p href="www.boot.dev"><a>greatgrand</a></p></h1></span>')

    def test_to_html_with_greatgrands(self):
        greatgrand_node2 = LeafNode("b", "greatgrand 2")
        greatgrand_node1 = LeafNode("a", "greatgrand")
        grandchild_node = ParentNode("p", [greatgrand_node1, greatgrand_node2], {"href": "www.boot.dev"})
        child_node = ParentNode("h1", [grandchild_node])
        parent_node = ParentNode("span", [child_node])
        self.assertEqual(parent_node.to_html(), '<span><h1><p href="www.boot.dev"><a>greatgrand</a><b>greatgrand 2</b></p></h1></span>')

    def test_to_html_with_twochild_greatgrand(self):
        greatgrand_node = LeafNode("a", "greatgrand")
        grandchild_node = ParentNode("p", [greatgrand_node], {"href": "www.boot.dev"})
        child_node2 = LeafNode(None, "Normal text")
        child_node = ParentNode("h1", [grandchild_node])
        parent_node = ParentNode("span", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), '<span><h1><p href="www.boot.dev"><a>greatgrand</a></p></h1>Normal text</span>')
    
    def test_to_html_with_two_child_parents(self):
        grandchild_node2 = LeafNode(None, "Normal text")
        child_node2 = ParentNode("div", [grandchild_node2])
        greatgrand_node = LeafNode("a", "greatgrand")
        grandchild_node = ParentNode("p", [greatgrand_node], {"href": "www.boot.dev"})
        child_node = ParentNode("h1", [grandchild_node])
        parent_node = ParentNode("span", [child_node, child_node2])
        self.assertEqual(parent_node.to_html(), '<span><h1><p href="www.boot.dev"><a>greatgrand</a></p></h1><div>Normal text</div></span>')

    def test_to_html_with_no_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", None)
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_no_tag(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode(None, [child_node])
        with self.assertRaises(ValueError):
            parent_node.to_html()

    def test_to_html_with_empty_list(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [])
        self.assertEqual(parent_node.to_html(), "<div></div>")

class TestHTMLConversion(unittest.TestCase):
    def test_text(self):
        node = TextNode("This is a text node", TextType.TEXT)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, None)
        self.assertEqual(html_node.value, "This is a text node")

    def test_link(self):
        node = TextNode("This is a link", TextType.LINK, "www.boot.dev")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "a")
        self.assertEqual(html_node.value, "This is a link")
        self.assertEqual(html_node.props, {"href":"www.boot.dev"})

    def test_image(self):
        node = TextNode("This is an image", TextType.IMAGE, "bootdev.png")
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "img")
        self.assertEqual(html_node.value, None)
        self.assertEqual(html_node.props, {"src":"bootdev.png", "alt":"This is an image"})

    def test_italic(self):
        node = TextNode("This is an italic text node", TextType.ITALIC)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "i")
        self.assertEqual(html_node.value, "This is an italic text node")

    def test_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "b")
        self.assertEqual(html_node.value, "This is a bold text node")

    def test_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        html_node = text_node_to_html_node(node)
        self.assertEqual(html_node.tag, "code")
        self.assertEqual(html_node.value, "This is a code text node")

class TestSplitDeliminator(unittest.TestCase):
    def test_text_with_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertEqual(new_nodes, [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ])

    def test_text_with_bold(self):
        node = TextNode("This is **text** with a **bold word**", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [
            TextNode("This is ", TextType.TEXT),
            TextNode("text", TextType.BOLD),
            TextNode(" with a ", TextType.TEXT),
            TextNode("bold word", TextType.BOLD),
        ])

    def test_text_with_italics(self):
        node = TextNode("_This_ is text with leading and trailing _italic words_", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "_", TextType.ITALIC)
        self.assertEqual(new_nodes, [        
            TextNode("This", TextType.ITALIC),
            TextNode(" is text with leading and trailing ", TextType.TEXT),
            TextNode("italic words", TextType.ITALIC),
        ])

    def test_text_with_all_bold(self):
        node = TextNode("This is all bold words", TextType.BOLD)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is all bold words", TextType.BOLD)])

    def test_text_with_two_nodes(self):
        node = TextNode("This is all bold words", TextType.BOLD)
        node2 = TextNode("This is a **bold** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node, node2], "**", TextType.BOLD)
        self.assertEqual(new_nodes, [TextNode("This is all bold words", TextType.BOLD),
                                    TextNode("This is a ", TextType.TEXT),
                                    TextNode("bold", TextType.BOLD),
                                    TextNode(" word", TextType.TEXT)])
        
    def test_text_with_missing(self):
        node = TextNode("This is text with a `code block word", TextType.TEXT)
        with self.assertRaises(Exception):
            split_nodes_delimiter([node], "`", TextType.CODE)

class TextRegexNonsense(unittest.TestCase):
    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

    def test_extract_markdown_links(self):
        matches = extract_markdown_links(
            "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        )
        self.assertListEqual([("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")], matches)

    def test_extract_markdown_mult_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and ![image2](https://i.imgur.com/zjjcJKZ2.png) and ![image3](https://i.imgur.com/zjjcJKZ3.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png"), ("image2", "https://i.imgur.com/zjjcJKZ2.png"), ("image3", "https://i.imgur.com/zjjcJKZ3.png")], matches)

    def test_split_images(self):
        node = TextNode(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png) and another ![second image](https://i.imgur.com/3elNhQu.png)",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("image", TextType.IMAGE, "https://i.imgur.com/zjjcJKZ.png"),
                TextNode(" and another ", TextType.TEXT),
                TextNode(
                    "second image", TextType.IMAGE, "https://i.imgur.com/3elNhQu.png"
                ),
            ],
            new_nodes,
        )

    def test_split_images_only_text(self):
        node = TextNode(
            "This is text without an image.",
            TextType.TEXT,
        )
        new_nodes = split_nodes_image([node])
        #print(new_nodes)
        self.assertListEqual(
            [
                TextNode("This is text without an image.", TextType.TEXT),
                
            ],
            new_nodes,
        )
    
    def test_split_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        #print(new_nodes)
        self.assertListEqual(
                [TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" and ", TextType.TEXT),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),], new_nodes)
        
    def test_split_backtoback_links(self):
        node = TextNode("This is text with a link [to boot dev](https://www.boot.dev)[to youtube](https://www.youtube.com/@bootdotdev)", TextType.TEXT,)
        new_nodes = split_nodes_link([node])
        print(new_nodes)
        self.assertListEqual(
                [TextNode("This is text with a link ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode("to youtube", TextType.LINK, "https://www.youtube.com/@bootdotdev"),], new_nodes)

if __name__ == "__main__":
    unittest.main()