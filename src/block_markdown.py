from inline_markdown import *
from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
from node_conversion import text_node_to_html_node
import re
from enum import Enum

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "# Heading"
    CODE = "``` code ```"
    QUOTE = "> block quote"
    UNORDERED_LIST = "- unordered list"
    ORDERED_LIST = "1. ordered list"

def markdown_to_blocks(markdown):
    split_to_lines = markdown.split("\n\n")
    filtered_lines = []
    for line in split_to_lines:
        if line == "":
            continue
        filtered_lines.append(line.strip())
    return filtered_lines

def block_to_block_type(block):
    lines = block.split("\n")
    if re.match(r"^#{1,6} ", block):
        return BlockType.HEADING
    elif block.startswith("```") and block.endswith("```"):
        return BlockType.CODE
    elif block.startswith(">"):
        for line in lines:
            if not line.startswith(">"):
                return BlockType.PARAGRAPH
        return BlockType.QUOTE
    elif block.startswith("- "):
        for line in lines:
            if not line.startswith("- "):
                return BlockType.PARAGRAPH
        return BlockType.UNORDERED_LIST
    elif block.startswith("1. "):
        i = 1
        for line in lines:
            if not line.startswith(f"{i}. "):
                return BlockType.PARAGRAPH
            i += 1
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH

def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    new_nodes = []
    for block in markdown_blocks:
        block_type = block_to_block_type(block)
        if block_type == BlockType.PARAGRAPH:
            strip_new_lines = re.sub(r"\n", " ", block)
            child_nodes = text_to_children(strip_new_lines)
            node = ParentNode("p", child_nodes)
            new_nodes.append(node)
        if block_type == BlockType.HEADING:
            strip_new_lines = re.sub(r"\n", " ", block)
            matches = re.findall(r"^#+", block)
            i = len(matches[0])
            heading_text = strip_new_lines[i:].strip()
            child_nodes = text_to_children(heading_text)
            node = ParentNode(f"h{i}", child_nodes)
            new_nodes.append(node)
        if block_type == BlockType.QUOTE:
            lines = block.split("\n")
            cleaned_lines = [line[1:].strip() if line.startswith(">") else line for line in lines]
            cleaned_block = " ".join(cleaned_lines)
            child_nodes = text_to_children(cleaned_block)
            node = ParentNode("blockquote", child_nodes)
            new_nodes.append(node)
        if block_type == BlockType.CODE:
            lines = block.splitlines()
            code_lines = lines[1:-1]
            code_text = "\n".join(code_lines) + "\n"
            node = TextNode(code_text, TextType.CODE)
            pre_node = ParentNode("pre", [text_node_to_html_node(node)])
            new_nodes.append(pre_node)
        if block_type == BlockType.UNORDERED_LIST:
            old_lines = block.split("\n")
            new_lines = list_to_children(old_lines)
            node = ParentNode("ul", new_lines)
            new_nodes.append(node)
        if block_type == BlockType.ORDERED_LIST:
            old_lines = block.split("\n")
            new_lines = list_to_children(old_lines)
            node = ParentNode("ol", new_lines)
            new_nodes.append(node)
    div_node = ParentNode("div", new_nodes)
    return div_node

def text_to_children(text):
    text_nodes = text_to_textnodes(text)
    html_nodes = []
    for node in text_nodes:
        html_node = text_node_to_html_node(node)
        html_nodes.append(html_node)
    return html_nodes

def list_to_children(old_lines):
    new_lines = []
    for line in old_lines:     
        if line.startswith("- "):
            child_nodes = text_to_children(line[2:].strip())
            node = ParentNode("li", child_nodes)
            new_lines.append(node)
        else:
            stripped_line = re.sub(r"^\d+\. ", "", line)
            child_nodes = text_to_children(stripped_line.strip())
            node = ParentNode("li", child_nodes)
            new_lines.append(node)
    return new_lines
    