from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[1:].strip(" ")
    raise Exception("Header 1 not found")

def generate_page(from_path, template_path, dest_path):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        from_contents = from_file.read()
    with open(template_path) as template_file:
        template_contents = template_file.read()
    page_nodes = markdown_to_html_node(from_contents)
    page_content = page_nodes.to_html()
    page_title = extract_title(from_contents)
    final_html = template_contents.replace("{{ Content }}", page_content)
    final_html = final_html.replace("{{ Title }}", page_title)
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)
    


    