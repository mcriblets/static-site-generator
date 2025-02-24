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
    old_nodes = [
        TextNode("this is a `text` node", TextType.CODE, "https://www.boot.dev"),
        TextNode("this is a text node", TextType.TEXT, "https://www.boot.dev"),
        TextNode("This is text with a `code block` word", TextType.TEXT)
    ]
    
    text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
    test_node = TextNode(text, TextType.TEXT)
    text_to_textnodes(test_node)
    
    
    
if __name__ == "__main__":
    main()