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
    italic_split = split_nodes_delimiter(bold_split, "_", TextType.ITALIC)
    italic_split = split_nodes_delimiter(italic_split, "*", TextType.ITALIC)
    code_split = split_nodes_delimiter(italic_split, "`", TextType.CODE)
    link_split = split_nodes_link(code_split)
    image_split = split_nodes_image(link_split)
    
    return image_split


def markdown_to_blocks(markdown):
    
    markdown = re.sub(r'\n\s+\n', '\n\n', markdown)
    
    markdown_split_list = []
    
    markdown_split = markdown.split("\n\n")
    
    for markdown in markdown_split:
        markdown = markdown.strip()
        if markdown != "":
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
 
 
def get_header_value(header_markdown):
    header_count = header_markdown.count('#')
    remove_header = re.sub(r'^#*\s', '', header_markdown)
     
    if header_count > 6:
        header_count = 6
        
    header_tag = "h" + str(header_count)
    
    return (header_tag, remove_header)


def remove_backticks(code_markdown):
    raw_code = code_markdown.strip("```")
    
    return raw_code


def remove_markdown_quotes(quote_markdown):
    raw_quote = re.sub(r'^>*\s', '', quote_markdown, flags=re.MULTILINE)
    
    raw_quote = raw_quote.strip()
    raw_quote = raw_quote.split('\n')
    raw_quote = " ".join(raw_quote)
    
    return raw_quote


def remove_unordered_list(list_markdown):
    raw_list = re.sub(r'^\* ', '', list_markdown, flags=re.MULTILINE)
    
    raw_list = raw_list.split("\n")
    
    filtered_list = list(filter(None, raw_list))
    
    return filtered_list


def remove_ordered_list(list_markdown):
    raw_list = re.sub(r'^\d+\. ', '', list_markdown, flags=re.MULTILINE)
    
    raw_list = raw_list.split("\n")
    
    filtered_list = list(filter(None, raw_list))
    
    return filtered_list


def text_to_children(text):
    textnode_list = text_to_textnodes(text)
    
    children_list = []
    
    for textnode in textnode_list:
        html_node = text_node_to_html_node(textnode)
        children_list.append(html_node)

    return children_list
    
    
            
def markdown_to_html_node(markdown):
    markdown_blocks = markdown_to_blocks(markdown)
    
    child_nodes = []
    
    for block in markdown_blocks:
        blocktype = block_to_blocktype(block)

        if blocktype == BlockType.HEADING:
            header_tag, content = get_header_value(block)
            children = text_to_children(content)
            node = HTMLNode(header_tag, None, children)
            child_nodes.append(node)
        elif blocktype == BlockType.CODE:
            content = remove_backticks(block)
            code_node = HTMLNode("code", content, None)
            node = HTMLNode("pre", None, [code_node])
            child_nodes.append(node)
        elif blocktype == BlockType.QUOTE:
            content = remove_markdown_quotes(block)
            children = text_to_children(content)
            node = HTMLNode("blockquote", None, children)
            child_nodes.append(node)
        elif blocktype == BlockType.UNORDERED_LIST:
            unordered_list_raw = remove_unordered_list(block)
            node_list = []
            for item in unordered_list_raw:
                children = text_to_children(item)
                node = HTMLNode("li", None, children)
                node_list.append(node)
            list_node = HTMLNode("ul", None, node_list)
            child_nodes.append(list_node)
        elif blocktype == BlockType.ORDERED_LIST:
            ordered_list_raw = remove_ordered_list(block)
            node_list = []
            for item in ordered_list_raw:
                children = text_to_children(item)
                node = HTMLNode("li", None, children)
                node_list.append(node)
            list_node = HTMLNode("ol", None, node_list)
            child_nodes.append(list_node)
        elif blocktype == BlockType.PARAGRAPH:
            block = re.sub(r'\s+', ' ', block)
            block = block.strip()
            children = text_to_children(block)
            node = HTMLNode("p", None, children)
            child_nodes.append(node)
        else:
            raise ValueError("Unknown Blocktype!")
        
    return HTMLNode("div", None, child_nodes)