import unittest

from htmlnode import HTMLNode


class TestHTMLNode(unittest.TestCase):
    def test_props_to_html_nothing(self):
        node = HTMLNode()
        self.assertEqual(node.props_to_html(), "")

    def test_props_to_html_one_prop(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
            }
        )
        self.assertEqual(node.props_to_html(),
                         ' href="https://www.google.com"')

    def test_props_to_html_more_props(self):
        node = HTMLNode(
            props={
                "href": "https://www.google.com",
                "target": "_blank",
            }
        )
        self.assertEqual(
            node.props_to_html(), ' href="https://www.google.com" target="_blank"'
        )

    def test_repr(self):
        node = HTMLNode("a", "this is a link", None, {
                        "href": "https://www.google.com"})
        self.assertEqual(
            f"{node}",
            "HTMLNode(a, this is a link, None, {'href': 'https://www.google.com'})",
        )


if __name__ == "__main__":
    unittest.main()
