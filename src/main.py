import re
import os
import shutil
import sys
from textnode import *
from htmlnode import *
from splitnodes import *


def copy_contents(source_directory, target_directory): 
    
    source_path = os.path.abspath(source_directory)
    target_path = os.path.abspath(target_directory) 
    
    if os.path.exists(target_path) == True:
        shutil.rmtree(target_directory) 
        
    os.mkdir(target_path)
    
    for file in os.listdir(source_path):
        source_file = os.path.join(source_path, file)
        target_file = os.path.join(target_path, file)
        
        if os.path.isfile(source_file) == True:
            shutil.copy(source_file, target_file)
        elif os.path.isdir(source_file) == True:
            os.mkdir(target_file)
            copy_contents(source_file, target_file)


def copy_contents_prime(source_directory, target_directory): 
    
    source_path = os.path.abspath(source_directory)
    target_path = os.path.abspath(target_directory) 
    
    if os.path.exists(target_path) == True:
        shutil.rmtree(target_directory) 
    
    shutil.copytree(source_path, target_path) 


def extract_title(markdown):
    h1 = markdown_to_html_node(markdown)

    for node in h1.children:
        if node.tag == "h1":
            return node.children[0].value
        
    raise Exception("No h1 header found!")


def generate_page(from_path, template_path, dest_path, basepath):
    print(f"Generating a page from {from_path} to {dest_path} using {template_path}!")
    
    source_file = open(from_path, "r")
    source_content = source_file.read()
    
    template_file = open(template_path, "r")
    template_content = template_file.read()
    
    nodes = markdown_to_html_node(source_content)
    html = nodes.to_html()
    
    page_title = extract_title(source_content)
    
    new_title = template_content.replace("{{ Title }}", page_title)
    new_content = new_title.replace("{{ Content }}", html)
    new_basepath = new_content.replace('href="/', 'href="' + basepath)

    new_src = new_basepath.replace('src="/', 'src="' + basepath)
    
    with open(dest_path, "w") as f:
        f.write(new_src)
    

def generate_multiple_pages(source_directory, template_path, target_directory, basepath):
    source_path = os.path.abspath(source_directory)
    target_path = os.path.abspath(target_directory)
    
    for file in os.listdir(source_path):
        source_file = os.path.join(source_path, file)
        target_file = os.path.join(target_path, file)
        
        if os.path.isfile(source_file) == True and source_file.endswith(".md"):
            print(source_file)
            target_file = target_file.replace(".md", ".html")
            generate_page(source_file, template_path, target_file, basepath)
        elif os.path.isdir(source_file) == True:
            os.mkdir(target_file)
            generate_multiple_pages(source_file, template_path, target_file, basepath)


def main():
    
    if len(sys.argv) == 2:
        basepath = sys.argv[1]
    else:
        basepath = "/"
    
    copy_contents("./static/", "./docs/")
    generate_multiple_pages("./content/", "./template.html", "./docs/", basepath)
        
if __name__ == "__main__":
    main()