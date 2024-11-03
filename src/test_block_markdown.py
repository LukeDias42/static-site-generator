import unittest

from block_markdown import markdown_to_blocks, block_to_block_type, BlockType


class TestBlockMarkdown(unittest.TestCase):
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
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

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
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

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
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_block_to_block_type_valid_unordered_lists(self):
        valid_unordered_lists = [
            "* item 1",
            "- item 1",
            "* item 1\n* item 2",
            "- item 1\n- item 2",
            "* item 1\n- item 2",
        ]

        for block in valid_unordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.UNORDERED_LIST)

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
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_block_to_block_type_valid_ordered_lists(self):
        valid_ordered_lists = [
            "1. item 1",
            "1. item 1\n2. item 2",
            "1. item 1\n2. item 2\n3. item 3",
        ]

        for block in valid_ordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.ORDERED_LIST)

    def test_block_to_block_type_invalid_ordered_lists(self):
        invalid_ordered_lists = [
            " 1. trailing space",
            "1- incorrectly formatted first item",
            "1. item 1\n3. incorrect order",
            "no list",
            "2. start incorrect",
        ]

        for block in invalid_ordered_lists:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_markdown_to_blocks_clean(self):
        markdown = """# This is a heading

This is a paragraph of text. It has some **bold** and *italic* words inside of it.

* This is the first list item in a list block
* This is a list item
* This is another list item"""

        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )

    def test_markdown_to_blocks_messy(self):
        markdown = """    # This is a heading


                This is a paragraph of text. It has some **bold** and *italic* words inside of it.                      
            
                






* This is the first list item in a list block           
* This is a list item               
        * This is another list item"""

        self.assertListEqual(
            markdown_to_blocks(markdown),
            [
                "# This is a heading",
                "This is a paragraph of text. It has some **bold** and *italic* words inside of it.",
                "* This is the first list item in a list block           \n* This is a list item               \n        * This is another list item",
            ],
        )


if __name__ == "__main__":
    unittest.main()
