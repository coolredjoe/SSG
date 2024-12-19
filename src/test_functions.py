import unittest
from functions import (
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    split_all_nodes,
    extract_markdown_images,
    extract_markdown_links,
    markdown_to_blocks,
    block_to_block_type,
)

from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_image_standard(self):
        string = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif)"
        result = extract_markdown_images(string)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])

    def test_multiple_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
        result = extract_markdown_images(text)
        self.assertEqual(
            result, 
            [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")]
        )
    
    def test_no_image(self):
        text = "htlksrhlkjwyposlflkjhtlkwahkjs"
        result = extract_markdown_images(text)
        result2 = extract_markdown_links(text)
        self.assertEqual(result, [])
        self.assertEqual(result2, [])

    def test_image_and_link(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev [to boot dev](https://www.boot.dev)"
        result = extract_markdown_images(text)
        result2 = extract_markdown_links(text)
        self.assertEqual(result, [("rick roll", "https://i.imgur.com/aKaOqIh.gif")])
        self.assertEqual(result2, [("to boot dev", "https://www.boot.dev")])

    def test_link_standard(self):
        string = "This is text with a [to boot dev](https://www.boot.dev)"
        result = extract_markdown_links(string)
        self.assertEqual(result, [("to boot dev", "https://www.boot.dev")])

    def test_multiple_img(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        result = extract_markdown_links(text)
        self.assertEqual(
            result, 
            [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")]
        )

    def test_delim_bold(self):
        node = TextNode("This is text with a **bolded** word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_double(self):
        node = TextNode(
            "This is text with a **bolded** word and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded", TextType.BOLD),
                TextNode(" word and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_bold_multiword(self):
        node = TextNode(
            "This is text with a **bolded word** and **another**", TextType.TEXT
        )
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("bolded word", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("another", TextType.BOLD),
            ],
            new_nodes,
        )

    def test_delim_italic(self):
        node = TextNode("This is text with an *italic* word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("This is text with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_delim_bold_and_italic(self):
        node = TextNode("**bold** and *italic*", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "**", TextType.BOLD)
        new_nodes = split_nodes_delimiter(new_nodes, "*", TextType.ITALIC)
        self.assertListEqual(
            [
                TextNode("bold", TextType.BOLD),
                TextNode(" and ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
            ],
            new_nodes,
        )

    def test_delim_code(self):
        node = TextNode("This is text with a `code block` word", TextType.TEXT)
        new_nodes = split_nodes_delimiter([node], "`", TextType.CODE)
        self.assertListEqual(
            [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" word", TextType.TEXT),
            ],
            new_nodes,
        )

    def test_split_imgs(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev ![to boot dev](https://www.boot.dev) hahaha"
        result = split_nodes_image([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" hahaha", TextType.TEXT)
            ]
        )
    
    def test_multi_node_list_img(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev ![to boot dev](https://www.boot.dev) hahaha"
        result = split_nodes_image([TextNode(text, TextType.TEXT), TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" hahaha", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev"),
                TextNode(" hahaha", TextType.TEXT)
            ]
        )        

    def test_multi_node_list_link(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev [to boot dev](https://www.boot.dev) hahaha"
        result = split_nodes_link([TextNode(text, TextType.TEXT), TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" hahaha", TextType.TEXT),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" hahaha", TextType.TEXT)
            ]
        )       

    def test_split_links(self):
        text = "This is text with a [rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev [to boot dev](https://www.boot.dev) hahaha"
        result = split_nodes_link([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.LINK, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
                TextNode(" hahaha", TextType.TEXT)
            ]
        )

    def test_split_only_link(self):
        text = "[to boot dev](https://www.boot.dev)"
        result = split_nodes_link([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev")
            ]
        )

    def test_split_only_img(self):
        text = "![to boot dev](https://www.boot.dev)"
        result = split_nodes_image([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("to boot dev", TextType.IMAGE, "https://www.boot.dev")
            ]
        )


    def test_empty(self):
        text = ""
        result = split_nodes_link([TextNode(text, TextType.TEXT)])
        result2 = split_nodes_image([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result,
            []
        )
        self.assertEqual(
            result2,
            []
        )

    def test_link_wo_link(self):
        text = "This is text with a and a link to bootdev ![to boot dev](https://www.boot.dev)"
        result = split_nodes_link([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result,
            [
                TextNode(text, TextType.TEXT)
            ]
        )

    def test_img_wo_img(self):
        text = "This is text with a and a link to bootdev [to boot dev](https://www.boot.dev)"
        result = split_nodes_image([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result,
            [
                TextNode(text, TextType.TEXT)
            ]
        )

    def test_both(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev [to boot dev](https://www.boot.dev)"
        result = split_nodes_image([TextNode(text, TextType.TEXT)])
        result2 = split_nodes_link([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev [to boot dev](https://www.boot.dev)", TextType.TEXT)
            ]
        )
        self.assertEqual(
            result2, [
                TextNode("This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.LINK, "https://www.boot.dev"),
            ]
        )

    def split_all(self):
        text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev [to boot dev](https://www.boot.dev)This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and a link to bootdev [to boot dev](https://www.boot.dev)"
        result = split_nodes_link(split_nodes_image([TextNode(text, TextType.TEXT)]))
        self.assertEqual(
            result, [
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.Link, "https://www.boot.dev"),
                TextNode("This is text with a ", TextType.TEXT),
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode(" and a link to bootdev ", TextType.TEXT),
                TextNode("to boot dev", TextType.Link, "https://www.boot.dev")
            ]
        )

    def split_all_no_text(self):
        text = "![rick roll](https://i.imgur.com/aKaOqIh.gif)[to boot dev](https://www.boot.dev)"
        result = split_nodes_link(split_nodes_image([TextNode(text, TextType.TEXT)]))
        self.assertEqual(
            result, [
                TextNode("rick roll", TextType.IMAGE, "https://i.imgur.com/aKaOqIh.gif"),
                TextNode("to boot dev", TextType.Link, "https://www.boot.dev")
            ]
        )       

    def test_split_all_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        result = split_all_nodes([TextNode(text, TextType.TEXT)])
        self.assertEqual(
            result, [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode("obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ]
        )

    def test_md_to_block(self):
        res = markdown_to_blocks("""# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item""")
        self.assertEqual(
            res, [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item"
            ]
        )
    
    def test_block_to_block_type(self):
        paragraph = "hello, this is a paragraph"
        heading2 = "# hello, this is a heading"
        heading = "###### hello, this is a heading too"
        not_a_heading3 = "####### hello, this sadly isn't a heading, (1 too many # so should be paragraph)"
        not_a_heading_either = "#This is not a heading too, since the # isn't followed by a space"
        code_block = "```this is a codeblock```"
        quote_block = "> this is a quote block"
        quote_block2 = "> this is a quote block too\n> real and true\n> no joke"
        not_a_quote = "> this may\nlook like a\nquote block\n> but isn't"
        not_a_quote2 = ">nor is this one"
        ul_block = "- this is a quote block"
        ul_block2 = "* this is a quote block too\n- real and true\n* no joke"
        not_a_ul = "* this may\nlook like a\nquote block\n* but isn't"
        not_a_ul2 = "*nor is this one"
        ol_block = "1. this is a quote block"
        ol_block2 = "1. this is a quote block too\n2. real and true\n3. no joke"
        not_a_ol = "1. this may\nlook like a\nquote block\n2. but isn't"
        not_a_ol2 = "1.nor is this one"
        self.assertEqual(block_to_block_type(paragraph), "paragraph")
        self.assertEqual(block_to_block_type(not_a_heading3), "paragraph")
        self.assertEqual(block_to_block_type(not_a_heading_either), "paragraph")
        self.assertEqual(block_to_block_type(not_a_quote), "paragraph")
        self.assertEqual(block_to_block_type(not_a_quote2), "paragraph")
        self.assertEqual(block_to_block_type(not_a_ul), "paragraph")
        self.assertEqual(block_to_block_type(not_a_ul2), "paragraph")
        self.assertEqual(block_to_block_type(not_a_ol), "paragraph")
        self.assertEqual(block_to_block_type(not_a_ol2), "paragraph")
        self.assertEqual(block_to_block_type(heading), "heading")
        self.assertEqual(block_to_block_type(heading2), "heading")
        self.assertEqual(block_to_block_type(code_block), "code")
        self.assertEqual(block_to_block_type(quote_block), "quote")
        self.assertEqual(block_to_block_type(quote_block2), "quote")
        self.assertEqual(block_to_block_type(ul_block), "unordered_list")
        self.assertEqual(block_to_block_type(ul_block2), "unordered_list")
        self.assertEqual(block_to_block_type(ol_block), "ordered_list")
        self.assertEqual(block_to_block_type(ol_block2), "ordered_list")
        


if __name__ == "__main__":
    unittest.main()