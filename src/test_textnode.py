import unittest

from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)
        
    def test_eq_2(self):
        node = TextNode("This is a test node", TextType.ITALIC)
        node2 = TextNode("this is a text node", TextType.TEXT, "http://boot.dev")
        self.assertNotEqual(node, node2)
        
    def test_eq_3(self):
        node = TextNode("U wot mate?", TextType.CODE)
        node2 = TextNode("U wot mate?", TextType.CODE, "http://google.com")
        self.assertNotEqual(node, node2)
        
    def test_eq_4(self):
        node = TextNode("Hello world!", TextType.ITALIC, "http://google.com")
        node2 = TextNode("Hello world!", TextType.ITALIC, "http://google.com")
        self.assertEqual(node, node2)


if __name__ == "__main__":
    unittest.main()