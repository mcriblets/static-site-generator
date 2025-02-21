import unittest

from htmlnode import *

class TestHTMLNode(unittest.TestCase):
    
    def test(self):
        props = {
        "href": "https://www.google.com",
        "target": "_blank",
    }
        node = HTMLNode(props=props)
        props_string =  ' href="https://www.google.com" target="_blank"'
        incorrect_props_string = 'href="https://www.google.com"target="_blank"'
    
        self.assertEqual(node.props_to_html(), props_string)
        self.assertNotEqual(node.props_to_html(), incorrect_props_string)
        
    
    def test2(self):
        props = {
            "blah": "blahblahblah",
            "bah": "_humbug",
            "u": "wot_mate"
        }
        
        node = HTMLNode(props=props)
        props_string = ' blah="blahblahblah" bah="_humbug" u="wot_mate"'
        incorrect_props_string = 'blah="blahblahblah"bah="_humbug"u="wot_mate"'
        
        self.assertEqual(node.props_to_html(), props_string)
        self.assertNotEqual(node.props_to_html(), incorrect_props_string)
        
    
    def test3(self):
        props = {
            "nuh": "_uh_",
            "stahp": "_it",
            "o": "rly_?",
            "nah": "rly",
            "srsly": "u_guys_"
        }
        
        node = HTMLNode(props=props)
        props_string = ' nuh="_uh_" stahp="_it" o="rly_?" nah="rly" srsly="u_guys_"'
        incorrect_props_string = 'nuh="_uh_" stahp="_it" o="rly_?" nah="rly" srsly="u_guys_"'
        
        self.assertEqual(node.props_to_html(), props_string)
        self.assertNotEqual(node.props_to_html(), incorrect_props_string)
        
        
class TestLeafNode(unittest.TestCase):
    
    def test(self):
        node = LeafNode("p", "This is a paragraph of text.")
        render_string = "<p>This is a paragraph of text.</p>"
        
        self.assertEqual(node.to_html(), render_string)
            
            
    def test2(self):
        node = LeafNode("a", "Click me!", {"href": "https://www.google.com"})
        render_string = '<a href="https://www.google.com">Click me!</a>'
        
        self.assertEqual(node.to_html(), render_string)
        
    
    def test3(self):
        node = LeafNode("a", "General Kenobi!", {"href": "https://www.well-hello-there.com"})
        render_string = '<a href="https://www.well-hello-there.com">General Kenobi!</a>'
        
        self.assertEqual(node.to_html(), render_string)
        
    
    def test4(self):
        node = LeafNode("b", "Kabal Wins!")
        render_string = '<p>Kabal Wins1</p>'
        
        self.assertNotEqual(node.to_html(), render_string)