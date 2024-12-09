from textnode import TextNode, TextType
import re

def split_nodes_delimiter(old_nodes, delimiter, text_type):
    result = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            result.append(old_node)
            continue
        sections = []
        slices = old_node.text.split(delimiter)
        if len(slices) % 2 == 0:
            raise ValueError("delimiter section not closed")
        for i in range(len(slices)):
            if slices[i] == "":
                continue
            if i % 2 == 0:
                sections.append(TextNode(slices[i], TextType.TEXT))
            else:
                sections.append(TextNode(slices[i], text_type))
        result.extend(sections)
    return result
        
def extract_markdown_images(text):
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return helper(text, pattern)

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    return helper(text, pattern)

def helper(text, pattern):
    matches = re.match(pattern, text)
    
