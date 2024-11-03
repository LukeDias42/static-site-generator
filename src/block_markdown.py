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
code_regex = r"^```[\s\S]*?\S[\s\S]*?```$"
unordered_list_regex = r"^[-*]\s+"


def block_to_block_type(block: str) -> BlockType:
    if re.match(heading_regex, block) and len(block.splitlines()) == 1:
        return BlockType.HEADING
    if re.match(code_regex, block):
        return BlockType.CODE
    if all(line.startswith(">") for line in block.splitlines()):
        return BlockType.QUOTE
    if all(re.match(unordered_list_regex, line) for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    if all(
        re.match(rf"^{index+1}\.\s+", line)
        for index, line in enumerate(block.splitlines())
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
