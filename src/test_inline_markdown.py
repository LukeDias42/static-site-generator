import unittest

from inline_markdown import (
    extract_markdown_images,
    extract_markdown_links,
    split_nodes_delimiter,
    split_nodes_image,
    split_nodes_link,
    text_to_textnodes,
)
from textnode import TextNode, TextType


class TestInlineMarkdown(unittest.TestCase):
    def test_text_to_text_nodes(self):
        text = "This is **text** with an *italic* word and a `code block` and an ![obi wan image](https://i.imgur.com/fJRm4Vk.jpeg) and a [link](https://boot.dev)"
        self.maxDiff = None
        self.assertEqual(
            text_to_textnodes(text),
            [
                TextNode("This is ", TextType.TEXT),
                TextNode("text", TextType.BOLD),
                TextNode(" with an ", TextType.TEXT),
                TextNode("italic", TextType.ITALIC),
                TextNode(" word and a ", TextType.TEXT),
                TextNode("code block", TextType.CODE),
                TextNode(" and an ", TextType.TEXT),
                TextNode(
                    "obi wan image", TextType.IMAGE, "https://i.imgur.com/fJRm4Vk.jpeg"
                ),
                TextNode(" and a ", TextType.TEXT),
                TextNode("link", TextType.LINK, "https://boot.dev"),
            ],
        )

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
        self.assertEqual(extract_markdown_images(
            text), [("an image", "imageurl.com")])

    def test_extract_markdown_images_with_many_images(self):
        text = "This is a text with ![an image](imageurl.com) and ![another image](imageurl.com/another)"
        self.assertEqual(
            extract_markdown_images(text),
            [("an image", "imageurl.com"),
             ("another image", "imageurl.com/another")],
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
        self.assertEqual(extract_markdown_links(
            text), [("a link", "google.com")])

    def test_extract_markdown_link_with_many_links(self):
        text = "This is a text with [a link](google.com) and [another link](boot.dev)"
        self.assertEqual(
            extract_markdown_links(text),
            [("a link", "google.com"), ("another link", "boot.dev")],
        )

    def test_split_nodes_image_nothing(self):
        nodes = [TextNode("This is just a text node", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("This is just a text node", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_one_image(self):
        nodes = [
            TextNode(
                "This is a text node with ![an image](imageurl.com).", TextType.TEXT
            )
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "imageurl.com"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_many_images(self):
        nodes = [
            TextNode(
                "This is a text node with ![an image](imageurl.com) and ![another image](imageurl.com/another).",
                TextType.TEXT,
            )
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "imageurl.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another image", TextType.IMAGE,
                         "imageurl.com/another"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_image_in_the_beginning(self):
        nodes = [
            TextNode(
                "![An image](imageurl.com)! Amazing.",
                TextType.TEXT,
            )
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("An image", TextType.IMAGE, "imageurl.com"),
                TextNode("! Amazing.", TextType.TEXT),
            ],
        )

    def test_split_nodes_image_many_nodes(self):
        nodes = [
            TextNode(
                "This is a text node with ![an image](imageurl.com).",
                TextType.TEXT,
            ),
            TextNode(
                "This is another text node with ![another image](imageurl.com/another).",
                TextType.TEXT,
            ),
        ]
        self.assertListEqual(
            split_nodes_image(nodes),
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("an image", TextType.IMAGE, "imageurl.com"),
                TextNode(".", TextType.TEXT),
                TextNode("This is another text node with ", TextType.TEXT),
                TextNode("another image", TextType.IMAGE,
                         "imageurl.com/another"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_nothing(self):
        nodes = [TextNode("This is just a text node", TextType.TEXT)]
        self.assertListEqual(
            split_nodes_link(nodes),
            [
                TextNode("This is just a text node", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_one_link(self):
        nodes = [
            TextNode(
                "This is a text node with [a link](google.com).", TextType.TEXT)
        ]
        self.assertListEqual(
            split_nodes_link(nodes),
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("a link", TextType.LINK, "google.com"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_many_links(self):
        nodes = [
            TextNode(
                "This is a text node with [an link](google.com) and [another link](boot.dev).",
                TextType.TEXT,
            )
        ]
        self.assertListEqual(
            split_nodes_link(nodes),
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("an link", TextType.LINK, "google.com"),
                TextNode(" and ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "boot.dev"),
                TextNode(".", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_link_in_the_beginning(self):
        nodes = [
            TextNode(
                "[An link](google.com) Amazing.",
                TextType.TEXT,
            )
        ]
        self.assertListEqual(
            split_nodes_link(nodes),
            [
                TextNode("An link", TextType.LINK, "google.com"),
                TextNode(" Amazing.", TextType.TEXT),
            ],
        )

    def test_split_nodes_link_many_nodes(self):
        nodes = [
            TextNode(
                "This is a text node with [an link](google.com).",
                TextType.TEXT,
            ),
            TextNode(
                "This is another text node with [another link](boot.dev).",
                TextType.TEXT,
            ),
        ]
        self.assertListEqual(
            split_nodes_link(nodes),
            [
                TextNode("This is a text node with ", TextType.TEXT),
                TextNode("an link", TextType.LINK, "google.com"),
                TextNode(".", TextType.TEXT),
                TextNode("This is another text node with ", TextType.TEXT),
                TextNode("another link", TextType.LINK, "boot.dev"),
                TextNode(".", TextType.TEXT),
            ],
        )


if __name__ == "__main__":
    unittest.main()
