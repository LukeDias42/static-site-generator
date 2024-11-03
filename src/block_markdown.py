from enum import Enum
import re


class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if len(block) >= 1]


heading_regex = r"^#{1,6}\s"
def block_to_block_type(block: str) -> BlockType:
    if re.match(heading_regex, block):
        return BlockType.HEADING
    return BlockType.PARAGRAPH
