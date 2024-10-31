from enum import Enum
from leafnode import LeafNode


class TextType(Enum):
    TEXT = "normal"
    BOLD = "bold"
    ITALIC = "italic"
    CODE = "code"
    LINK = "link"
    IMAGE = "image"


class TextNode:
    def __init__(self, text, text_type, url=None):
        self.text = text
        self.text_type = text_type.value
        self.url = url

    def __eq__(self, other) -> bool:
        return (
            self.text == other.text
            and self.text_type == other.text_type
            and self.url == other.url
        )

    def __repr__(self) -> str:
        return f"TextNode({self.text}, {self.text_type}, {self.url})"


def text_node_to_html_node(text_node):
    if text_node.text_type == TextType.TEXT.value:
        return LeafNode(text_node.text)
    if text_node.text_type == TextType.BOLD.value:
        return LeafNode(text_node.text, "b")
    if text_node.text_type == TextType.ITALIC.value:
        return LeafNode(text_node.text, "i")
    if text_node.text_type == TextType.CODE.value:
        return LeafNode(text_node.text, "code")
    if text_node.text_type == TextType.LINK.value:
        return LeafNode(text_node.text, "a", {"href": text_node.url})
    if text_node.text_type == TextType.IMAGE.value:
        return LeafNode("", "img", {"src": text_node.url, "alt": text_node.text})
    raise ValueError("Unkown Text Type")
