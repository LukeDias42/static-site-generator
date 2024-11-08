from collections.abc import Sequence
import unittest

from block_markdown import (
    extract_code_from_block,
    extract_heading_from_block,
    extract_ordered_list_from_block,
    extract_quotes_from_block,
    extract_unordered_list_from_block,
    markdown_to_blocks,
    block_to_block_type,
    BlockType,
    markdown_to_html,
)
from leafnode import LeafNode
from parentnode import ParentNode


class TestBlockMarkdown(unittest.TestCase):
    def test_markdown_to_html(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

```
# A fancy code block~~
```

## This is another heading for the list:

* This is the first item
* This is the second item
- This is **another** list item

### This is another heading for the ordered list:

1. This is the first item
2. `This is another fancy code~~`
3. Too many *cool* items!"""

        self.assertEqual(
            markdown_to_html(markdown),
            [
                LeafNode("This is a heading", "h1"),
                ParentNode(
                    "p",
                    [
                        LeafNode("This is a paragraph of text. It has some "),
                        LeafNode("bold", "b"),
                        LeafNode(" and "),
                        LeafNode("italic", "i"),
                        LeafNode(" words inside of it."),
                    ],
                ),
                ParentNode("pre", [LeafNode("# A fancy code block~~", "code")]),
                LeafNode("This is another heading for the list:", "h2"),
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("This is the first item")]),
                        ParentNode("li", [LeafNode("This is the second item")]),
                        ParentNode(
                            "li",
                            [
                                LeafNode("This is "),
                                LeafNode("another", "b"),
                                LeafNode(" list item"),
                            ],
                        ),
                    ],
                ),
                LeafNode("This is another heading for the ordered list:", "h3"),
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode("This is the first item")]),
                        ParentNode(
                            "li", [LeafNode("This is another fancy code~~", "code")]
                        ),
                        ParentNode(
                            "li",
                            [
                                LeafNode("Too many "),
                                LeafNode("cool", "i"),
                                LeafNode(" items!"),
                            ],
                        ),
                    ],
                ),
            ],
        )

    def test_extract_heading_from_block(self):
        test_cases: list[tuple[str, str, str]] = [
            # block, tag, value
            ("# heading 1", "h1", "heading 1"),
            ("## heading 2", "h2", "heading 2"),
            ("### heading 3", "h3", "heading 3"),
            ("#### heading 4", "h4", "heading 4"),
            ("##### heading 5", "h5", "heading 5"),
            ("###### heading 6", "h6", "heading 6"),
        ]
        for test_case in test_cases:
            with self.subTest(block=test_case[0]):
                block = test_case[0]
                leaf_node = extract_heading_from_block(block)
                self.assertEqual(leaf_node.tag, test_case[1])
                self.assertEqual(leaf_node.value, test_case[2])

    def test_extract_heading_from_block_incorrect(self):
        invalid_blocks = [
            "######## heading 7",
            " # heading after space",
            "###heading without space",
            "no heading at all",
            "# Multiline heading makes\nno sense",
        ]
        for block in invalid_blocks:
            with self.subTest(block=block):
                self.assertRaises(ValueError, extract_heading_from_block, block)

    def test_extract_quotes_from_block(self):
        test_cases: list[tuple[str, ParentNode]] = [
            # block, expected
            ("> quote", ParentNode("quoteblock", [LeafNode("quote")])),
            (">quote", ParentNode("quoteblock", [LeafNode("quote")])),
            (
                ">quote 1\n> quote 2",
                ParentNode("quoteblock", [LeafNode("quote 1"), LeafNode("quote 2")]),
            ),
            (">", ParentNode("quoteblock", [])),
            (">>>>", ParentNode("quoteblock", [LeafNode(">>>")])),
        ]
        for test_case in test_cases:
            with self.subTest(block=test_case[0]):
                block = test_case[0]
                quote_node = extract_quotes_from_block(block)
                self.assertEqual(quote_node, test_case[1])

    def test_extract_quotes_from_block_incorrect(self):
        invalid_blocks = [
            "no greater than",
            " > incorrect formatting",
            "< incorrect symbol",
        ]
        for block in invalid_blocks:
            with self.subTest(block=block):
                self.assertRaises(ValueError, extract_quotes_from_block, block)

    def test_extract_code_from_block(self):
        test_cases: list[tuple[str, ParentNode]] = [
            # block, expected
            (
                '```print("Hello, World!")```',
                ParentNode("pre", [LeafNode('print("Hello, World!")', "code")]),
            ),
            (
                '```python\ndef main():\n  print("Hello, World!")\nmain()\n```',
                ParentNode(
                    "pre",
                    [
                        LeafNode(
                            'python\ndef main():\n  print("Hello, World!")\nmain()',
                            "code",
                        )
                    ],
                ),
            ),
        ]
        for test_case in test_cases:
            with self.subTest(block=test_case[0]):
                block = test_case[0]
                code_node = extract_code_from_block(block)
                self.assertEqual(code_node, test_case[1])

    def test_extract_code_from_block_incorrect(self):
        invalid_blocks = [
            "``````",
            "```\n```",
            '```print("Hello, World!")``',
            '``print("Hello, World!")```',
            'print("Hello, World!")',
        ]
        for block in invalid_blocks:
            with self.subTest(block=block):
                self.assertRaises(ValueError, extract_code_from_block, block)

    def test_extract_ul_from_block(self):
        test_cases: list[tuple[str, ParentNode]] = [
            # block, expected
            ("- item 1", ParentNode("ul", [ParentNode("li", [LeafNode("item 1")])])),
            (
                "- **bold item**",
                ParentNode("ul", [ParentNode("li", [LeafNode("bold item", "b")])]),
            ),
            (
                "- mixed **bold item** and *italic* item.",
                ParentNode(
                    "ul",
                    [
                        ParentNode(
                            "li",
                            [
                                LeafNode("mixed "),
                                LeafNode("bold item", "b"),
                                LeafNode(" and "),
                                LeafNode("italic", "i"),
                                LeafNode(" item."),
                            ],
                        )
                    ],
                ),
            ),
            (
                "- item 1\n- item 2\n* item 3",
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", [LeafNode("item 1")]),
                        ParentNode("li", [LeafNode("item 2")]),
                        ParentNode("li", [LeafNode("item 3")]),
                    ],
                ),
            ),
            (
                "- \n- \n* ",
                ParentNode(
                    "ul",
                    [
                        ParentNode("li", []),
                        ParentNode("li", []),
                        ParentNode("li", []),
                    ],
                ),
            ),
        ]
        for test_case in test_cases:
            with self.subTest(block=test_case[0]):
                block = test_case[0]
                ul_node = extract_unordered_list_from_block(block)
                self.assertEqual(ul_node, test_case[1])

    def test_extract_ul_from_block_incorrect(self):
        invalid_blocks = [
            " - incorrect formating",
            "# incorrect symbol",
            "-too close",
            "--",
        ]
        for block in invalid_blocks:
            with self.subTest(block=block):
                self.assertRaises(ValueError, extract_unordered_list_from_block, block)

    def test_extract_ol_from_block(self):
        test_cases: list[tuple[str, ParentNode]] = [
            # block, expected
            ("1. item 1", ParentNode("ol", [ParentNode("li", [LeafNode("item 1")])])),
            (
                "1. item 1\n2. item 2",
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", [LeafNode("item 1")]),
                        ParentNode("li", [LeafNode("item 2")]),
                    ],
                ),
            ),
            (
                "1. \n2. ",
                ParentNode(
                    "ol",
                    [
                        ParentNode("li", []),
                        ParentNode("li", []),
                    ],
                ),
            ),
        ]
        for test_case in test_cases:
            with self.subTest(block=test_case[0]):
                block = test_case[0]
                leaf_node = extract_ordered_list_from_block(block)
                self.assertEqual(leaf_node, test_case[1])

    def test_extract_ol_from_block_incorrect(self):
        invalid_blocks = [
            " 1. incorrect formating",
            ".1 incorrect formating",
            "1- incorrect symbol",
            "1.too close",
            "2. starting incorrectly",
            "0. starting incorrectly",
        ]
        for block in invalid_blocks:
            with self.subTest(block=block):
                self.assertRaises(ValueError, extract_ordered_list_from_block, block)

    def test_block_to_block_type_valid_headings(self):
        valid_headings = [
            "# heading 1",
            "## heading 2",
            "### heading 3",
            "#### heading 4",
            "##### heading 5",
            "###### heading 6",
        ]
        for block in valid_headings:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.HEADING)

    def test_block_to_block_type_invalid_headings(self):
        invalid_headings = [
            "######## heading 7",
            " # heading after space",
            "###heading without space",
            "no heading at all",
            "# Multiline heading makes\nno sense",
        ]
        for block in invalid_headings:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_valid_codes(self):
        valid_codes = [
            "```inline code```",
            "```python\nprint('Hello, World!')```",
            "```python\nprint('Hello, World!')\n```",
            "```python\ndef main():\n  print('Hello, World!')\n```",
        ]
        for block in valid_codes:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.CODE)

    def test_block_to_block_type_invalid_codes(self):
        invalid_codes = [
            "``missing backtick start```",
            "```missing backtick end``",
            "no back tick",
            "``````",
            "```        ```",
            "```\t\n\r\n```",
        ]
        for block in invalid_codes:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_valid_quotes(self):
        valid_quotes = [
            "> A single quote",
            "> First quote\n> Second quote",
            "> A quote\n>\n> An empty and another quote",
            ">\n>\n>\n>",
            ">Very close quote",
        ]
        for block in valid_quotes:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.QUOTE)

    def test_block_to_block_type_invalid_quotes(self):
        invalid_quotes = [
            " > trailing space",
            "no quote",
            "a > start without >",
        ]
        for block in invalid_quotes:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_valid_unordered_lists(self):
        valid_unordered_lists = [
            "* ",
            "- ",
            "* item 1",
            "- item 1",
            "* item 1\n* item 2",
            "- item 1\n- item 2",
            "* item 1\n- item 2",
        ]

        for block in valid_unordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.UNORDERED_LIST)

    def test_block_to_block_type_invalid_unordered_lists(self):
        invalid_unordered_lists = [
            "** incorrect symbol",
            "no items",
            "* correct item\n-- incorrect item",
            "-incorrect item",
            "    * incorrect item",
        ]

        for block in invalid_unordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_block_to_block_type_valid_ordered_lists(self):
        valid_ordered_lists = [
            "1. item 1",
            "1. ",
            "1. item 1\n2. item 2",
            "1. item 1\n2. item 2\n3. item 3",
        ]

        for block in valid_ordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_lists(self):
        invalid_ordered_lists = [
            " 1. trailing space",
            "1.too close",
            "1- incorrectly formatted first item",
            "1. item 1\n3. incorrect order",
            "no list",
            "2. start incorrect",
        ]

        for block in invalid_ordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(block), BlockType.PARAGRAPH)

    def test_markdown_to_blocks_clean(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        expected: Sequence[str] = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
        ]

        self.assertEqual(markdown_to_blocks(markdown), expected)

    def test_markdown_to_blocks_messy(self):
        markdown = """    # This is a heading


                This is a paragraph of text. It has some **bold** and *italic* words inside of it.








* This is the first list item in a list block\t\t\t
* This is a list item\t
        * This is another list item"""

        blocks = markdown_to_blocks(markdown)
        expected: Sequence[str] = [
            "# This is a heading",
            "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
            "* This is the first list item in a list block\t\t\t\n* This is a list item\t\n        * This is another list item",
        ]
        self.assertEqual(blocks, expected)


if __name__ == "__main__":
    unittest.main()
