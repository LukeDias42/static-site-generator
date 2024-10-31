import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
)
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

    def test_extract_markdown_images_with_nothing(self):
        text = "This is just a plain text"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_images_with_image(self):
        text = "This is a text with ![an image](imageurl.com)"
        self.assertEqual(extract_markdown_images(text), [("an image", "imageurl.com")])

    def test_extract_markdown_images_with_many_images(self):
        text = "This is a text with ![an image](imageurl.com) and ![another image](imageurl.com/another)"
        self.assertEqual(
            extract_markdown_images(text),
            [("an image", "imageurl.com"), ("another image", "imageurl.com/another")],
        )

    def test_extract_markdown_images_with_link(self):
        text = "This is a text with [a link](google.com)"
        self.assertEqual(extract_markdown_images(text), [])

    def test_extract_markdown_link_with_nothing(self):
        text = "This is just a plain text"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_link_with_image(self):
        text = "This is a text with ![an image](imageurl.com)"
        self.assertEqual(extract_markdown_links(text), [])

    def test_extract_markdown_link_with_link(self):
        text = "This is a text with [a link](google.com)"
        self.assertEqual(extract_markdown_links(text), [("a link", "google.com")])

    def test_extract_markdown_link_with_many_links(self):
        text = "This is a text with [a link](google.com) and [another link](boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("a link", "google.com"), ("another link", "boot.dev")],
        )


if __name__ == "__main__":
    unittest.main()
