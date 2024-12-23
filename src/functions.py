from textnode import TextNode, TextType
from htmlnode import HTMLNode, LeafNode, ParentNode
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
    pattern = r"!\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = []
    for node in old_nodes:
        text = node.text
        index = 0
        matches = re.finditer(pattern, text)
        
        for match in matches:
            if text[index: match.start()] != "":
                result.append(TextNode(text[index: match.start()], node.text_type, node.url))
            img_section = extract_markdown_images(text[match.start(): match.end()])
            result.append(TextNode(img_section[0][0], TextType.IMAGE, img_section[0][1]))
            index = match.end()
        if text[index:] != "":
            result.append(TextNode(text[index:], node.text_type, node.url))

    return result


def split_nodes_link(old_nodes):
    pattern = r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)"
    result = []
    for node in old_nodes:
        text = node.text
        index = 0
        matches = re.finditer(pattern, text)
        
        for match in matches:
            if text[index: match.start()] != "":
                result.append(TextNode(text[index: match.start()], node.text_type, node.url))
            link_section = extract_markdown_links(text[match.start(): match.end()])
            result.append(TextNode(link_section[0][0], TextType.LINK, link_section[0][1]))
            index = match.end()
        if text[index:] != "":
            result.append(TextNode(text[index:], node.text_type, node.url))
    
    return result


def split_all_nodes(old_nodes):
    return split_nodes_link(split_nodes_image(split_nodes_delimiter(split_nodes_delimiter(split_nodes_delimiter(old_nodes, "**", TextType.BOLD), "*", TextType.ITALIC), "`", TextType.CODE)))


def markdown_to_blocks(markdown):
    markdown_strings = markdown.split("\n\n")
    result = [i.strip() for i in markdown_strings if i != ""]
    return result

def block_to_block_type(block):
    heading_pattern = r"^#{1,6} .*"
    
    if bool(re.search(heading_pattern, block)):
        return "heading"
    elif block.startswith("```") and block.endswith("```"):
        return "code"
    elif check_newline_followed_by_char(block, r"^> "):
        return "quote"
    elif check_newline_followed_by_char(block, r"^[*|-] "):
        return "unordered_list"
    elif check_newline_followed_by_char(block, r"^\d+\. "):  
        return "ordered_list"
    else:
        return "paragraph"

def check_newline_followed_by_char(text, char):
    lines = text.split('\n')
    for line in lines:
        if not bool(re.search(char, line)):
            return False
    return True

def markdown_to_html_node(markdown):
    blocks_ls = markdown_to_blocks(markdown)
    nodes = []
    for block in blocks_ls:
        block_type = block_to_block_type(block)
        match block_type:
            case "paragraph":
                node = paragraph(block)
            case "code":
                node = LeafNode("code", block)
            case "heading":
                node = LeafNode("h", block)
            case "ordered_list":
                pass
            case "unordered_list":
                pass
            case "quote":
                pass
            case _:
                pass


def paragraph(block):
    return LeafNode("p", block)

def code(block):
    