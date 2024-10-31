import unittest

from inline_markdown import split_nodes_delimiter
from textnode import TextNode, TextType


class TestTextNode(unittest.TestCase):
    def test_split_nodes_delimiter_bold(self):
        nodes = [TextNode("This is a **bold** text node", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(nodes, "**", TextType.BOLD),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_many_bold(self):
        nodes = [
            TextNode(
                "This is a **bold**, **very bold**, **extremely bold** text node",
                TextType.TEXT,
            )
        ]
        self.assertListEqual(
            split_nodes_delimiter(nodes, "**", TextType.BOLD),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("very bold", TextType.BOLD),
                TextNode(", ", TextType.TEXT),
                TextNode("extremely bold", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_italic(self):
        nodes = [TextNode("This is a *italic* text node", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(nodes, "*", TextType.ITALIC),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_code(self):
        nodes = [TextNode("This is a `code` text node", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_delimiter(nodes, "`", TextType.CODE),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text node", TextType.TEXT),
            ],
        )

    def test_split_nodes_delimiter_many_old_nodes(self):
        nodes = [
            TextNode("This is a **bold** text node", TextType.TEXT),
            TextNode("This is a `code` text node", TextType.TEXT),
            TextNode("This is a *italic* text node", TextType.TEXT),
        ]
        self.assertListEqual(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter(nodes, "**", TextType.BOLD),
                    "*",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            ),
            [
                TextNode("This is a ", TextType.TEXT),
                TextNode("bold", TextType.BOLD),
                TextNode(" text node", TextType.TEXT),
                TextNode("This is a ", TextType.TEXT),
                TextNode("code", TextType.CODE),
                TextNode(" text node", TextType.TEXT),
                TextNode("This is a ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" text node", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
