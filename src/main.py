from textnode import TextNode, TextType
from htmlnode import HTMLNode
from page_generator import generate_page, generate_pages_recursive
import os
import shutil
import sys

def main():
    print("Checking for existing contents")
    source_path = "./static"
    dest_path = "./docs"
    content_path = "./content"
    template_path = "./template.html"
    if os.path.exists(dest_path):
        print("Deleting existing directory")
        shutil.rmtree(dest_path)

    if len(sys.argv) > 1:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    copy_directory_contents(source_path, dest_path)

    generate_pages_recursive(content_path, template_path, dest_path, basepath)

def copy_directory_contents(source, dest):
    if not os.path.exists(dest):
        print(f"Creating new {dest} directory")
        os.mkdir(dest)
    directory_list = os.listdir(source)
    for item in directory_list:
        old_filepath = os.path.join(source, item)
        new_filepath = os.path.join(dest, item)
        if os.path.isfile(old_filepath):
            print(f"Copying {old_filepath} to {new_filepath}")
            shutil.copy(old_filepath, new_filepath)
        if os.path.isdir(old_filepath):
            print(f"Creating directory: {new_filepath}")
            os.mkdir(new_filepath)
            copy_directory_contents(old_filepath, new_filepath)



if __name__ == "__main__":
    main()