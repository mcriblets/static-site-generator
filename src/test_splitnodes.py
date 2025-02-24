import unittest

from htmlnode import *
from textnode import *
from splitnodes import *

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
        image_test = [TextNode(Plain text only, normal, None)]
        
        self.assertEqual(len(image_nodes), len(image_test))
        self.assertEqual(image_nodes, image_test)