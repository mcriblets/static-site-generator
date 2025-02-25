import re
from textnode import *
from htmlnode import *
from splitnodes import *


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT:
        html_node = LeafNode(None, text_node.text)
    elif text_node.text_type == TextType.BOLD:
        html_node = LeafNode("b", text_node.text)
    elif text_node.text_type == TextType.ITALIC:
        html_node = LeafNode("i", text_node.text)
    elif text_node.text_type == TextType.CODE:
        html_node = LeafNode("code", text_node.text)
    elif text_node.text_type == TextType.LINK:
        html_node = LeafNode("a", text_node.text, {"href": text_node.url})
    elif text_node.text_type == TextType.IMAGE:
        html_node = LeafNode("img", "", {"src": text_node.url, "alt": text_node.text})
    else:
        raise Exception("Not a supported TextType.")
    return html_node


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