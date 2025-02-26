import unittest

from main import *

class TestExtractTitle(unittest.TestCase):
    
    def test(self):
        title = extract_title("# Hello\n\n## Hello")
        
        self.assertEqual(title, "Hello")
        
    
    def test2(self):
        with self.assertRaises(Exception) as exc:
            title = extract_title("## Hello\n\n## Hello")
            
        self.assertEqual(str(exc.exception), "No h1 header found!")
        
        
    def test3(self):
        title = extract_title("## Hello\n\n# Hello")
        
        self.assertEqual(title, "Hello")
        
        
    def test4(self):
        title = extract_title("# Hello\n\n# NOT YOU")
        
        self.assertEqual(title, "Hello")