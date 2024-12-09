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
    matches = re.findall(pattern, text)
    return matches

def extract_markdown_links(text):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    matches = re.findall(pattern, text)
    return matches

def split_nodes_image(old_nodes):
    pattern = r"!\[([^\]]*)\]\(([^)]+)\)"
    result = []
    for node in old_nodes:
        text = node.text
        index = 0
        matches = re.finditer(pattern, text)
        
        for match in matches:
            img_section = extract_markdown_images(text[match.start(): match.end()])
            result.append(TextNode(img_section[0][0], TextType.IMAGE, img_section[0][1]))
            if text[index: match.start()] != "":
                result.append(TextNode(text[index: match.start()], TextType.TEXT))
            index = match.end()
        if text[index:] != "":
            result.append(TextNode(text[index:], TextType.TEXT))
    
    return result


def split_nodes_link(old_nodes):
    pattern = r"\[([^\]]*)\]\(([^)]+)\)"
    result = []
    for node in old_nodes:
        text = node.text
        index = 0
        matches = re.finditer(pattern, text)
        
        for match in matches:
            link_section = extract_markdown_links(text[match.start(): match.end()])
            result.append(TextNode(link_section[0][0], TextType.LINK, link_section[0][1]))
            if text[index: match.start()] != "":
                result.append(TextNode(text[index: match.start()], TextType.TEXT))
            index = match.end()
        if text[index:] != "":
            result.append(TextNode(text[index:], TextType.TEXT))
    
    return result
