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
    clean_markdown = "\n".join([line.strip()
                               for line in markdown.splitlines()])
    return [block.strip() for block in clean_markdown.split("\n\n") if len(block) >= 1]
