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