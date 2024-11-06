from collections.abc import Sequence
from enum import Enum
import re

from htmlnode import HTMLNode
from inline_markdown import text_to_textnodes
from parentnode import ParentNode
from leafnode import LeafNode
from textnode import text_nodes_to_html_nodes
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


def markdown_to_html(markdown: str) -> Sequence[HTMLNode]:
    return [block_to_html(block) for block in markdown_to_blocks(markdown)]


def markdown_to_blocks(markdown: str) -> Sequence[str]:
    return [block.strip() for block in markdown.split("\n\n") if len(block) >= 1]


def block_to_html(block: str) -> HTMLNode:
    block_type = block_to_block_type(block)
    if block_type == BlockType.HEADING:
        return extract_heading_from_block(block)
    elif block_type == BlockType.QUOTE:
        return extract_quotes_from_block(block)
    elif block_type == BlockType.CODE:
        return extract_code_from_block(block)
    elif block_type == BlockType.UNORDERED_LIST:
        return extract_unordered_list_from_block(block)


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
        re.match(rf"^{index+1}\. .*", line)
        for index, line in enumerate(block.splitlines())
    ):
        return BlockType.ORDERED_LIST
    return BlockType.PARAGRAPH


def extract_heading_from_block(block: str) -> LeafNode:
    matches = re.search(heading_regex, block)
    if matches is None:
        raise ValueError("Invalid heading")
    number_sign_amount = len(matches.group(1))
    text = matches.group(2)
    return LeafNode(text, f"h{number_sign_amount}")


def extract_quotes_from_block(block: str) -> ParentNode:
    quotes = block.splitlines()
    children = []
    for quote in quotes:
        matches = re.search(quote_regex, quote)
        if matches is None:
            raise ValueError(f"Invalid quote: {quote}")
        if matches.group(1) == "":
            continue
        children.extend(text_to_leaf_nodes(matches.group(1)))
    return ParentNode("quoteblock", children)


def extract_code_from_block(block: str) -> ParentNode:
    matches = re.search(code_regex, block)
    if matches is None:
        raise ValueError("Invalid code")
    text = matches.group(1)
    code = LeafNode(text, "code")
    return ParentNode("pre", [code])


def extract_unordered_list_from_block(block: str) -> ParentNode:
    children: list[HTMLNode] = []
    for item in block.splitlines():
        matches = re.search(unordered_list_regex, item)
        if matches is None:
            raise ValueError("Invalid unordered list")
        item_text = matches.group(1)
        children.append(ParentNode("li", text_to_leaf_nodes(item_text)))
    return ParentNode("ul", children)


def text_to_leaf_nodes(text: str) -> Sequence[HTMLNode]:
    if text == "":
        return []
    text_nodes = text_to_textnodes(text)
    if not text_nodes:
        raise ValueError("Something went wrong when trying to get text nodes")
    return text_nodes_to_html_nodes(text_nodes)
