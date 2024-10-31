import unittest

from textnode import TextNode, TextType, text_node_to_html_node


class TestTextNode(unittest.TestCase):
    def test_eq(self):
        node = TextNode("This is a text node", TextType.BOLD)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(node, node2)

    def test_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(node, node2)

    def test_not_eq(self):
        node = TextNode("This is a text node", TextType.ITALIC)
        node2 = TextNode("This is a text node", TextType.BOLD)
        self.assertNotEqual(node, node2)

    def test_not_eq_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        node2 = TextNode("This is a text node", TextType.BOLD, "yahoo.com")
        self.assertNotEqual(node, node2)

    def test_correct_repr(self):
        node = TextNode("This is a text node", TextType.BOLD)
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, None)")

    def test_correct_repr_with_url(self):
        node = TextNode("This is a text node", TextType.BOLD, "google.com")
        self.assertEqual(f"{node}", "TextNode(This is a text node, bold, google.com)")

    def test_text_node_to_html_node_normal(self):
        node = TextNode("This is a text node", TextType.TEXT)
        self.assertEqual(
            f"{text_node_to_html_node(node)}",
            "HTMLNode(None, This is a text node, None, None)",
        )

    def test_text_node_to_html_node_bold(self):
        node = TextNode("This is a bold text node", TextType.BOLD)
        self.assertEqual(
            f"{text_node_to_html_node(node)}",
            "HTMLNode(b, This is a bold text node, None, None)",
        )

    def test_text_node_to_html_node_italic(self):
        node = TextNode("This is a italic text node", TextType.ITALIC)
        self.assertEqual(
            f"{text_node_to_html_node(node)}",
            "HTMLNode(i, This is a italic text node, None, None)",
        )

    def test_text_node_to_html_node_code(self):
        node = TextNode("This is a code text node", TextType.CODE)
        self.assertEqual(
            f"{text_node_to_html_node(node)}",
            "HTMLNode(code, This is a code text node, None, None)",
        )

    def test_text_node_to_html_node_link(self):
        node = TextNode("This is a link text node", TextType.LINK, "google.com")
        self.assertEqual(
            f"{text_node_to_html_node(node)}",
            "HTMLNode(a, This is a link text node, None, {'href': 'google.com'})",
        )

    def test_text_node_to_html_node_url(self):
        node = TextNode("This is an image node", TextType.IMAGE, "image_link.com")
        self.assertEqual(
            f"{text_node_to_html_node(node)}",
            "HTMLNode(img, , None, {'src': 'image_link.com', 'alt': 'This is an image node'})",
        )


if __name__ == "__main__":
    unittest.main()
