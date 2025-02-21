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
        
            