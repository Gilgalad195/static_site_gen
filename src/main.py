from textnode import TextNode, TextType
from htmlnode import HTMLNode

def main():
    dummy_text_node = TextNode("anchor text", "link", "https://www.google.com")
    print (dummy_text_node.__repr__())

    dummy_html_node = HTMLNode("<tag>", "value of text string", None, {"href": "www.test.com"})
    print (dummy_html_node.__repr__())

main()