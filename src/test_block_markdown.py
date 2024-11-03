import unittest

from block_markdown import markdown_to_blocks
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
        ]
        for block in invalid_headings:
            with self.subTest(block=block):
                self.assertEqual(block_to_block_type(
                    block), BlockType.PARAGRAPH)

    def test_markdown_to_blocks_clean(self):
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
                "* This is the first list item in a list block\n* This is a list item\n* This is another list item",
            ],
        )


if __name__ == "__main__":
    unittest.main()
