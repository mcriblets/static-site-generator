from textnode import *

def main():
    test_node = TextNode("this is a text node", TextType.BOLD_TEXT, "https://www.boot.dev")
    
    print(test_node)
    
if __name__ == "__main__":
    main()