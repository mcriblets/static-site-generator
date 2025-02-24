import re

from textnode import *
from htmlnode import *

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


def extract_markdown_images(text):
    matches = re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches


def extract_markdown_links(text):
    matches = re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    
    return matches


def split_nodes_image(old_nodes):
    
    split_nodes_list = []
    
    for old_node in old_nodes:
        matches = extract_markdown_images(old_node.text)
        
        if not matches:
            split_nodes_list.append(TextNode(old_node.text, TextType.TEXT))
        else:
            first_match = matches[0]
            sections = old_node.text.split(f"![{first_match[0]}]({first_match[1]})", 1)
            
            if sections[0] == "":
                pass
            else:
                split_nodes_list.append(TextNode(sections[0], TextType.TEXT))

            split_nodes_list.append(TextNode(first_match[0], TextType.LINK, first_match[1]))
            
            if sections[1] != "":
                remaining_nodes = split_nodes_image([TextNode(sections[1], TextType.TEXT)])
                split_nodes_list.extend(remaining_nodes)
            else:
                pass
            
    return split_nodes_list
            


def split_nodes_link(old_nodes):
    
    split_nodes_list = []
    
    for old_node in old_nodes:
        matches = extract_markdown_links(old_node.text)
        
        if not matches:
            split_nodes_list.append(TextNode(old_node.text, TextType.TEXT))
        else:
            first_match = matches[0]
            sections = old_node.text.split(f"[{first_match[0]}]({first_match[1]})", 1)
            
            if sections[0] == "":
                pass
            else:
                split_nodes_list.append(TextNode(sections[0], TextType.TEXT))

            split_nodes_list.append(TextNode(first_match[0], TextType.LINK, first_match[1]))
            
            if sections[1] != "":
                remaining_nodes = split_nodes_link([TextNode(sections[1], TextType.TEXT)])
                split_nodes_list.extend(remaining_nodes)
            else:
                pass
            
    return split_nodes_list

            
