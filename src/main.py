from textnode import TextNode, TextType

def main():
    node = TextNode("This is a text node", TextType.BOLD, "https://www.boot.dev")
    node2 = TextNode("This is a text node", TextType.BOLD)
    print(node.__repr__(), node.__eq__(node2))

if __name__ == "__main__":
    main()
