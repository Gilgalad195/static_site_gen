from block_markdown import markdown_to_html_node
from htmlnode import HTMLNode, LeafNode, ParentNode
from pathlib import Path
import os

def extract_title(markdown):
    lines = markdown.split("\n")
    for line in lines:
        if line.startswith("# "):
            return line[2:].strip()
    raise Exception("Header 1 not found")

def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating page from {from_path} to {dest_path} using {template_path}")
    with open(from_path) as from_file:
        from_contents = from_file.read()
    with open(template_path) as template_file:
        template_contents = template_file.read()
    page_nodes = markdown_to_html_node(from_contents)
    page_content = page_nodes.to_html()
    page_title = extract_title(from_contents)
    add_content = template_contents.replace("{{ Content }}", page_content)
    add_title = add_content.replace("{{ Title }}", page_title)
    add_basepath = add_title.replace('href="/', f'href="{basepath}')
    final_html = add_basepath.replace('src="/', f'src="{basepath}')
    dest_dir = os.path.dirname(dest_path)
    os.makedirs(dest_dir, exist_ok=True)
    with open(dest_path, 'w') as dest_file:
        dest_file.write(final_html)

def generate_pages_recursive(dir_path_content, template_path, dest_dir_path, basepath):
    dir_list = os.listdir(dir_path_content)
    for entry in dir_list:
        entry_path = os.path.join(dir_path_content, entry)
        dest_path = os.path.join(dest_dir_path, entry)
        if os.path.isfile(entry_path):
            dest_file_path = Path(dest_path).with_suffix(".html")
            generate_page(entry_path, template_path, str(dest_file_path), basepath)
        else:
            generate_pages_recursive(entry_path, template_path, dest_path, basepath)
    


    