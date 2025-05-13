from enum import Enum
from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    new_nodes = []
    for node in old_nodes:
        if node.text_type != TextType.TEXT:
            new_nodes.append(node)
        else:
            split_text = node.text.split(delimiter)
            if len(split_text) % 2 == 0:
                raise Exception(f"invalid markdown: no closing delimiter for {delimiter}")
            temp_list = []
            for i, fragment in enumerate(split_text):
                if fragment == "":
                    continue
                if i % 2 != 1:
                    temp_list.append(TextNode(fragment, node.text_type))
                else:
                    temp_list.append(TextNode(fragment, text_type))
            new_nodes.extend(temp_list)
    return new_nodes

def extract_markdown_images(text):
    images = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return images

def extract_markdown_links(text):
    links = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    return links

def split_nodes_image(old_nodes):
    new_nodes = []
    for node in old_nodes:
        image_extracts = extract_markdown_images(node.text)
        if len(image_extracts) == 0:
            new_nodes.append(node)
        else:
            first_split = re.split(r"(!\[[^\[\]]*\]\([^\(\)]*\))", node.text)
            temp_list = []
            for i in range(len(first_split)):
                if first_split[i] == "":
                    continue
                if i % 2 != 1:
                    temp_list.append(TextNode(first_split[i], node.text_type))
                else:
                    strip_markdown = extract_markdown_images(first_split[i])
                    temp_list.append(TextNode(strip_markdown[0][0], TextType.IMAGE, strip_markdown[0][1]))
            new_nodes.extend(temp_list)
    return new_nodes

def split_nodes_link(old_nodes):
    new_nodes = []
    for node in old_nodes:
        link_extracts = extract_markdown_links(node.text)
        if len(link_extracts) == 0:
            new_nodes.append(node)
        else:
            first_split = re.split(r"(?<!!)(\[[^\[\]]*\]\([^\(\)]*\))", node.text)
            temp_list = []
            for i in range(len(first_split)):
                if first_split[i] == "":
                    continue
                if i % 2 != 1:
                    temp_list.append(TextNode(first_split[i], node.text_type))
                else:
                    strip_markdown = extract_markdown_links(first_split[i])
                    if len(strip_markdown[0]) != 2:
                        raise ValueError("invalid markdown section not closed properly")
                    else:
                        temp_list.append(TextNode(strip_markdown[0][0], TextType.LINK, strip_markdown[0][1]))
            new_nodes.extend(temp_list)
    return new_nodes

def text_to_textnodes(text):

    split_bold = split_nodes_delimiter(text, "**", TextType.BOLD)
    split_italic = split_nodes_delimiter(split_bold, "_", TextType.ITALIC)
    split_code = split_nodes_delimiter(split_italic, "`", TextType.CODE)
    split_images = split_nodes_image(split_code)
    split_links = split_nodes_link(split_images)

    return split_links