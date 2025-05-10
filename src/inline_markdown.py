from enum import Enum
from textnode import TextNode, TextType

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