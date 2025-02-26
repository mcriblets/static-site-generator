import re
from textnode import *
from htmlnode import *
from splitnodes import *


def main():
    markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item
    """
    
    print(markdown)
    markdown_split = markdown_to_blocks(markdown)
    
if __name__ == "__main__":
    main()