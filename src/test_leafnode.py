import unittest

from leafnode import LeafNode


class TestLeafNode(unittest.TestCase):
    def test_to_html_no_value(self):
        node = LeafNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_value_no_tag(self):
        node = LeafNode("this is a leaf node")
        self.assertEqual(node.to_html(), "this is a leaf node")

    def test_to_html_no_props(self):
        node = LeafNode("this is a leaf node", "p")
        self.assertEqual(node.to_html(), "<p>this is a leaf node</p>")

    def test_to_html_with_props(self):
        node = LeafNode(
            "this is a leaf node",
            "a",
            {
                "href": "https://www.google.com",
                "target": "_blank",
            },
        )
        self.assertEqual(
            node.to_html(),
            '<a href="https://www.google.com" target="_blank">this is a leaf node</a>',
        )


if __name__ == "__main__":
    unittest.main()
