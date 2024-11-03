import unittest

from parentnode import ParentNode
from leafnode import LeafNode


class TestParentNode(unittest.TestCase):
    def test_to_html_no_tag(self):
        node = ParentNode(None, None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_no_children(self):
        node = ParentNode("h1", None)
        self.assertRaises(ValueError, node.to_html)

    def test_to_html_with_leaf_child(self):
        node = ParentNode("h1", [LeafNode("this is a leaf node")])
        self.assertEqual(node.to_html(), "<h1>this is a leaf node</h1>")

    def test_to_html_with_complete_leaf_child(self):
        node = ParentNode(
            "h1",
            [
                LeafNode(
                    "this is a leaf node",
                    "a",
                    {
                        "href": "https://www.google.com",
                        "target": "_blank",
                    },
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<h1><a href="https://www.google.com" target="_blank">this is a leaf node</a></h1>',
        )

    def test_to_html_with_parent_child(self):
        node = ParentNode(
            "h1",
            [
                ParentNode(
                    "h2",
                    [
                        LeafNode(
                            "this is a leaf node",
                            "a",
                            {
                                "href": "https://www.google.com",
                                "target": "_blank",
                            },
                        ),
                    ],
                )
            ],
        )
        self.assertEqual(
            node.to_html(),
            '<h1><h2><a href="https://www.google.com" target="_blank">this is a leaf node</a></h2></h1>',
        )


if __name__ == "__main__":
    unittest.main()
