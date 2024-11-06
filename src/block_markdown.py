from enum import Enum
import re

heading_regex = r"^(#{1,6}) ([^\n]+)$"
code_regex = r"^```\s*?(\S[\s\S]*?)```$"
unordered_list_regex = r"^[-*] (.*)"
quote_regex = r"^>\s?(.*)"

class BlockType(Enum):
    PARAGRAPH = "paragraph"
    HEADING = "heading"
    CODE = "code"
    QUOTE = "quote"
    UNORDERED_LIST = "unordered_list"
    ORDERED_LIST = "ordered_list"


def markdown_to_blocks(markdown: str) -> list[str]:
    return [block.strip() for block in markdown.split("\n\n") if len(block) >= 1]




def block_to_block_type(block: str) -> BlockType:
    if re.match(heading_regex, block):
        return BlockType.HEADING
    if re.match(code_regex, block):
        return BlockType.CODE
    if all(re.match(quote_regex, line) for line in block.splitlines()):
        return BlockType.QUOTE
    if all(re.match(unordered_list_regex, line) for line in block.splitlines()):
        return BlockType.UNORDERED_LIST
    if all(
        re.match(rf"^{index+1}\.\s+", line)
        for index, line in enumerate(block.splitlines())
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH
