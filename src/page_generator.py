from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip(" ")
    raise Exception("Header 1 not found")