class HTMLNode():
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError
    
    def props_to_html(self):
        result = ""
        if self.props == None:
            return result
        for i in self.props:
            result += f" {i}=\"{self.props[i]}\""
        return result
    
    def __repr__(self):
        return f"{self.tag}\n{self.value}\n{self.children}\n{self.props}"


class LeafNode(HTMLNode):
    def __init__(self, tag=None, value=None, props=None):
        super().__init__(tag, value, None, props)
        
    def to_html(self):
        if self.value == None:
            raise ValueError("All leaf nodes must have a value.")
        if self.tag == None:
            return self.value
        return f"<{self.tag + self.props_to_html()}>{self.value}</{self.tag}>"
    

class ParentNode(HTMLNode):
    def __init__(self, tag=None, children=None, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self):
        result = ""
        if self.tag == None:
            raise ValueError("Tag can not be None")
        if self.children == None:
            raise ValueError("Children can not be None")
        for i in self.children:
            result += i.to_html()
        return f"<{self.tag}{self.props_to_html()}>" + result + f"</{self.tag}>"
        

        