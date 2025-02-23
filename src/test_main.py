import unittest

from htmlnode import *
from textnode import *
from main import *

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