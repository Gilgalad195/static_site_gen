from textnode import TextNode, TextType
from htmlnode import HTMLNode
import os
import shutil

def main():
    print("Checking for existing contents")
    source = "./static"
    dest = "./public"
    if os.path.exists(dest):
        print("Deleting existing directory")
        shutil.rmtree(dest)
    print(f"Creating new {dest} directory")
    os.mkdir(dest)
    copy_directory_contents(source, dest)

def copy_directory_contents(source, dest):
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



main()