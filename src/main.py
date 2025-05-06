from textnode import TextNode, TextType

def main():
    dummy_node = TextNode("anchor text", "link", "https://www.google.com")
    print (dummy_node.__repr__())

main()