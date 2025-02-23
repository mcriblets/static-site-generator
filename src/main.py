from textnode import *
from htmlnode import *


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


def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    split_nodes_list = []
    
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            split_nodes_list.append(old_node)
        else:
            new_nodes = old_node.text.split(delimiter)
            if len(new_nodes) == 1:
                split_nodes_list.append(TextNode(new_nodes[0], TextType.TEXT))
            elif len(new_nodes) == 3:
                split_nodes_list.append(TextNode(new_nodes[0], TextType.TEXT))
                split_nodes_list.append(TextNode(new_nodes[1], text_type))
                split_nodes_list.append(TextNode(new_nodes[2], TextType.TEXT))
            else:
                raise Exception("Delimiter mismatch found!  No closing delimiter found!")
    
    return split_nodes_list


def main():
    test_node = TextNode("this is a text node", TextType.TEXT, "https://www.boot.dev")
    
    old_nodes = [
        TextNode("this is a `text` node", TextType.CODE, "https://www.boot.dev"),
        TextNode("this is a text node", TextType.TEXT, "https://www.boot.dev"),
        TextNode("This is text with a `code block` word", TextType.TEXT)
    ]
    
    split_nodes_delimiter(old_nodes, "`", TextType.TEXT)
    
    
if __name__ == "__main__":
    main()