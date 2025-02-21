class HTMLNode():
    def __init__ (self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value 
        self.children = children
        self.props = props 
    
    def to_html(self):
        raise NotImplementedError("uh oh, spaghetti-os")
    
    def props_to_html(self):
        props_string = ""
        if self.props:
            for key, value in self.props.items():
                props_string += f' {key}="{value}"'
        return props_string
            
        
    def __repr__(self):
        html_node = self.__class__.__name__ 
        return f"HTMLNode({self.tag,}, {self.value}, {self.children}, {self.props})"
    

class LeafNode(HTMLNode):
    def __init__(self, tag, value, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        leaf_string = ""
        if not self.value:
            raise ValueError("All Leaf Nodes must have a value.")
        elif not self.tag:
            return str(self.value)
        else:
            leaf_string = f'<{self.tag}{self.props_to_html()}>{self.value}</{self.tag}>'
        
        return leaf_string
    

class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)
        
    def to_html(self):
        parent_string = ""
        if not self.tag:
            raise ValueError("All Parent Nodes must have a tag.")
        elif not self.children:
            raise ValueError("No children argument presented.")
        else:
            parent_string = f'<{self.tag}{self.props_to_html()}>'
            for node in self.children:
                parent_string += node.to_html()
         
        parent_string += f'</{self.tag}>'       
        return parent_string