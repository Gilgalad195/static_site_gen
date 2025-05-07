from enum import Enum

class HTMLNode:
    def __init__(self, tag=None, value=None, children=None, props=None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplemented
    
    def props_tohtml(self):
        # make list > populate list > join list on space characters > string output
        if self.props == None or self.props == {}:
            return ""
        properties_list = []
        for key, value in self.props.items():
            properties_list.append(f'{key}="{value}"')
        return " " + " ".join(properties_list)
    
    def __repr__(self):
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"