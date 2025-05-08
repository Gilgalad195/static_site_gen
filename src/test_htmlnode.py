import unittest

from htmlnode import HTMLNode, LeafNode, ParentNode

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

if __name__ == "__main__":
    unittest.main()