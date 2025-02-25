import re

from enum import Enum
from textnode import *
from htmlnode import *

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"
    

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    
    split_nodes_list = []
    
    for old_node in old_nodes:
        if old_node.text_type is not TextType.TEXT:
            split_nodes_list.append(old_node)
        else:
            new_nodes = old_node.text.split(delimiter)
            if len(new_nodes) == 1:
                if new_nodes[0]:  # Only append if not empty
                    split_nodes_list.append(TextNode(new_nodes[0], TextType.TEXT))
            elif len(new_nodes) == 3:
                if new_nodes[0]:
                    split_nodes_list.append(TextNode(new_nodes[0], TextType.TEXT))
                if new_nodes[1]:
                    node = TextNode(new_nodes[1], text_type)
                    split_nodes_list.append(TextNode(new_nodes[1], text_type))
                if new_nodes[2]:
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
            split_nodes_list.append(TextNode(old_node.text, old_node.text_type))
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
            split_nodes_list.append(TextNode(old_node.text, old_node.text_type))
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

            
def text_to_textnodes(text):

    text_nodes = [TextNode(text, TextType.TEXT)]

    bold_split = split_nodes_delimiter(text_nodes, "**", TextType.BOLD)
    italic_split = split_nodes_delimiter(bold_split, "*", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    link_split = split_nodes_link(code_split)
    image_split = split_nodes_image(link_split)
    
    return image_split


def markdown_to_blocks(markdown):
    
    markdown = re.sub(r'\n\s+\n', '\n\n', markdown)
    
    markdown_split_list = []
    
    markdown_split = markdown.split("\n\n")
    
    for markdown in markdown_split:
        if markdown != "":
            markdown = markdown.strip()
            markdown_split_list.append(markdown)
    
    return markdown_split_list
    

def is_ordered_list(lines):
    for i, line in enumerate(lines, start=1):
        expected_start = str(i) + ". "
        if not line.startswith(expected_start):
            return False
    return True


def block_to_blocktype(markdown):
    
    lines = markdown.split("\n")
    
    if markdown.startswith(("# ", "## ", "### ", "#### ", "##### ", "###### ")):
        return BlockType.HEADING
    elif markdown.startswith("```") and markdown.endswith("```"):
        return BlockType.CODE
    elif all(line.startswith(">") for line in lines):
        return BlockType.QUOTE
    elif all(line.startswith(("* ", "- ")) for line in lines):
        return BlockType.UNORDERED_LIST
    elif is_ordered_list(lines):
        return BlockType.ORDERED_LIST
    else:
        return BlockType.PARAGRAPH
            
        