import unittest

from htmlnode import *
from textnode import *
from splitnodes import *
from textwrap import dedent

class TestSplitNodes(unittest.TestCase):
    
    def test(self):
        old_nodes = [
        TextNode("Hello world", TextType.TEXT, "https://www.boot.dev")
    ]
        new_node_list = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
        self.assertEqual(len(new_node_list), 1)
        
        
    def test2(self):
        with self.assertRaises(Exception) as exc:
            old_nodes = [
            TextNode("Hello `world", TextType.TEXT, "https://www.boot.dev")
        ]
        
            new_node_list = split_nodes_delimiter(old_nodes, "`", TextType.CODE)
            
        self.assertEqual(str(exc.exception), "Delimiter mismatch found!  No closing delimiter found!")
        
    
    def test3(self):
         node = TextNode("This is text with a `code block` word", TextType.TEXT)
         new_node_list = split_nodes_delimiter([node], "`", TextType.CODE)
         expected_list = [
            TextNode("This is text with a ", TextType.TEXT),
            TextNode("code block", TextType.CODE),
            TextNode(" word", TextType.TEXT),
        ]
         
         self.assertEqual(len(new_node_list), len(expected_list))
         self.assertEqual(new_node_list, expected_list)
         
    
    def test4(self):
        with self.assertRaises(Exception) as exc:
            old_nodes = [
            TextNode("**Hello* world", TextType.TEXT, "https://www.boot.dev")
        ]
        
            new_node_list = split_nodes_delimiter(old_nodes, "**", TextType.BOLD)
            
        self.assertEqual(str(exc.exception), "Delimiter mismatch found!  No closing delimiter found!")
        
        
    def test5(self):
        with self.assertRaises(Exception) as exc:
            old_nodes = [
            TextNode("*Hello** world", TextType.TEXT, "https://www.boot.dev")
        ]
        
            new_node_list = split_nodes_delimiter(old_nodes, "*", TextType.ITALIC)
            
        self.assertEqual(str(exc.exception), "Delimiter mismatch found!  No closing delimiter found!")
        
        
class TestExtract(unittest.TestCase):
    
    def test(self):
        
        extract = extract_markdown_images("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)")
        extract_tuples = [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        
        self.assertEqual(extract, extract_tuples)
        self.assertEqual(len(extract), len(extract_tuples))
        
        
    def test2(self):
        
        extract = extract_markdown_links("This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)")
        extract_tuples = [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        
        self.assertEqual(extract, extract_tuples)
        self.assertEqual(len(extract), len(extract_tuples))
        

class TestSplitNodesLink(unittest.TestCase):
    
    def test(self):
        
        node = TextNode("Here is a [link](https://example.com)", TextType.TEXT)
        link_nodes = split_nodes_link([node])
        link_test = [TextNode("Here is a ", TextType.TEXT, None), TextNode("link", TextType.LINK, "https://example.com")]
        
        self.assertEqual(len(link_nodes), 2)
        self.assertEqual(link_nodes, link_test)
        
    
    def test2(self):
        
        node = TextNode("[link1](url1) and [link2](url2)", TextType.TEXT)
        link_nodes = split_nodes_link([node])
        link_test = [TextNode("link1", TextType.LINK, "url1"), TextNode(" and ", TextType.TEXT, None), TextNode("link2", TextType.LINK, "url2")]
        
        self.assertEqual(len(link_nodes), len(link_test))
        self.assertEqual(link_nodes, link_test)
        
    
    def test3(self):
        
        node = TextNode("Start [link1](url1) middle [link2](url2) end", TextType.TEXT)
        link_nodes = split_nodes_link([node])
        link_test = [TextNode("Start ", TextType.TEXT, None), TextNode("link1", TextType.LINK, "url1"), TextNode(" middle ", TextType.TEXT, None), TextNode("link2", TextType.LINK, "url2"), TextNode(" end", TextType.TEXT, None)]
        
        self.assertEqual(len(link_nodes), len(link_test))
        self.assertEqual(link_nodes, link_test)
        
        
    def test4(self):
        
        node = TextNode("Plain text only", TextType.TEXT)
        link_nodes = split_nodes_link([node])
        link_test = [TextNode("Plain text only", TextType.TEXT)]
        
        self.assertEqual(len(link_nodes), len(link_test))
        self.assertEqual(link_nodes, link_test)
        
        
    def test5(self):
        
        node = TextNode("", TextType.TEXT)
        link_nodes = split_nodes_link([node])
        link_test = [TextNode("", TextType.TEXT)]
        
        self.assertEqual(len(link_nodes), len(link_test))
        self.assertEqual(link_nodes, link_test)
        
        
class TestSplitNodesImage(unittest.TestCase):
    
    def test(self):
        
        node = TextNode("Here is an ![alt](image.jpg)", TextType.TEXT)
        image_nodes = split_nodes_image([node])
        image_test = [TextNode("Here is an ", TextType.TEXT, None), TextNode("alt", TextType.LINK, "image.jpg")]
        
        self.assertEqual(len(image_nodes), len(image_test))
        self.assertEqual(image_nodes, image_test)
        
        
    def test2(self):
        
        node = TextNode("![img1](url1.jpg) and ![img2](url2.jpg)", TextType.TEXT)
        image_nodes = split_nodes_image([node])
        image_test = [TextNode("img1", TextType.LINK, "url1.jpg"), TextNode(" and ", TextType.TEXT, None), TextNode("img2", TextType.LINK, "url2.jpg")]
        
        self.assertEqual(len(image_nodes), len(image_test))
        self.assertEqual(image_nodes, image_test)
        

    def test3(self):
        
        node = TextNode("Start ![img1](url1.jpg) middle ![img2](url2.jpg) end", TextType.TEXT)
        image_nodes = split_nodes_image([node])
        image_test = [TextNode("Start ", TextType.TEXT, None), TextNode("img1", TextType.LINK, "url1.jpg"), TextNode(" middle ", TextType.TEXT, None), TextNode("img2", TextType.LINK, "url2.jpg"), TextNode(" end", TextType.TEXT, None)]
        
        self.assertEqual(len(image_nodes), len(image_test))
        self.assertEqual(image_nodes, image_test)
        
    
    def test4(self):
        
        node = TextNode("Plain text only", TextType.TEXT)
        image_nodes = split_nodes_image([node])
        image_test = [TextNode("Plain text only", TextType.TEXT, None)]
        
        self.assertEqual(len(image_nodes), len(image_test))
        self.assertEqual(image_nodes, image_test)
        

class TestTexttoTextNodes(unittest.TestCase):
    
    def test(self):
        
        text = "Hello World!"
        conversion = text_to_textnodes(text)
        expected_output = [TextNode("Hello World!", TextType.TEXT, None)]
        
        self.assertEqual(conversion, expected_output)
        
        
    def test2(self):
        
        text = "Hello **world**"
        conversion = text_to_textnodes(text)
        expected_output = [TextNode("Hello ", TextType.TEXT, None), TextNode("world", TextType.BOLD, None)]
        
        self.assertEqual(conversion, expected_output)
        
        
    def test3(self):
        
        text = "Hello **world** with *italic*"
        conversion = text_to_textnodes(text)
        expected_output = [TextNode("Hello ", TextType.TEXT, None), TextNode("world", TextType.BOLD, None), TextNode(" with ", TextType.TEXT, None), TextNode("italic", TextType.ITALIC, None)]
        
        self.assertEqual(conversion, expected_output)
        
    
    def test4(self):
        
        text = "Click [here](https://boot.dev)"
        conversion = text_to_textnodes(text)
        expected_output = [TextNode("Click ", TextType.TEXT, None), TextNode("here", TextType.LINK, None)]
        
        self.assertEqual(conversion, expected_output)
        
        
class TestMarkdowntoBlocks(unittest.TestCase):
    
    def test(self):
        markdown = """# This is a heading

            This is a paragraph of text. It has some **bold** and *italic* words inside of it.

            * This is the first list item in a list block
            * This is a list item
            * This is another list item
                """
        markdown_blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(len(markdown_blocks), 3)
        
        
    def test2(self):
        markdown = "This is a single block"
        expected = ["This is a single block"]
        markdown_blocks = markdown_to_blocks(markdown)
        
        self.assertEqual(markdown_blocks, expected)
        
    
    def test3(self):
        markdown = """# This is a heading

            ## This is a paragraph of text with a header. It has some **bold** and *italic* words inside of it.

            ### This is the first list item in a list block
            
            #### This is a list item
            
            ##### This is another list item
                """
                
        markdown_blocks = markdown_to_blocks(markdown)
        self.assertEqual(len(markdown_blocks), 5)
        
        
class TestBlocktoBlockType(unittest.TestCase):
    
    def test(self):
        markdown_block = "# Test Heading"
        blocktype = block_to_blocktype(markdown_block)
        
        self.assertEqual(blocktype, BlockType.HEADING)
        
        
    def test2(self):
        markdown_block = "### Test Heading"
        blocktype = block_to_blocktype(markdown_block)
        
        self.assertEqual(blocktype, BlockType.HEADING)
        
        
    def test3(self):
        markdown_block = "###### Test Heading"
        blocktype = block_to_blocktype(markdown_block)
        
        self.assertEqual(blocktype, BlockType.HEADING)
        
        
    def test4(self):
        markdown_block = "```Test Code Block```"
        blocktype = block_to_blocktype(markdown_block)
        
        self.assertEqual(blocktype, BlockType.CODE)
        
        
    def test5(self):
        markdown_block = ">Testing\n>Quote\n>Did it work?"
        blocktype = block_to_blocktype(markdown_block)

        self.assertEqual(blocktype, BlockType.QUOTE)
        
        
    def test6(self):
        markdown_block = "* Testing\n* Unordered List\n* Did it work?"
        blocktype = block_to_blocktype(markdown_block)

        self.assertEqual(blocktype, BlockType.UNORDERED_LIST)
        
        
    def test7(self):
        markdown_block = "1. Testing\n2. Ordered List\n3. Did it work?"
        blocktype = block_to_blocktype(markdown_block)

        self.assertEqual(blocktype, BlockType.ORDERED_LIST)
        
        
class TestMarkdowntoHTMLNode(unittest.TestCase):
    
    def test_paragraphs(self):
        md = dedent("""
        This is **bolded** paragraph
        text in a p
        tag here

        This is another paragraph with _italic_ text and `code` here

        """)

        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>This is <b>bolded</b> paragraph text in a p tag here</p><p>This is another paragraph with <i>italic</i> text and <code>code</code> here</p></div>",
        )
        
    def test_mixed_lists(self):
        md = dedent("""
            1. First ordered item
            2. Second ordered item

            * Unordered item 1
            * Unordered item 2
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><ol><li>First ordered item</li><li>Second ordered item</li></ol><ul><li>Unordered item 1</li><li>Unordered item 2</li></ul></div>"
        )
        
        
    def test_separate_formatting(self):
        md = dedent("""
            # This is a heading with **bold** and _italic_ separately
            """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><h1>This is a heading with <b>bold</b> and <i>italic</i> separately</h1></div>"
        )
        
    def test_blockquote(self):
        md = dedent("""
    > This is a quote
    > with **bold** text
    > across multiple lines
    """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><blockquote>This is a quote with <b>bold</b> text across multiple lines</blockquote></div>"
        )
        
        
    def test_multiple_paragraphs_with_whitespace(self):
        md = dedent("""

    First paragraph
    with multiple lines

        Second paragraph
        with extra spaces

    """)
        node = markdown_to_html_node(md)
        html = node.to_html()
        self.assertEqual(
            html,
            "<div><p>First paragraph with multiple lines</p><p>Second paragraph with extra spaces</p></div>"
        )