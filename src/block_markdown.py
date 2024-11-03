from textnode import TextNode, TextType


def markdown_to_blocks(markdown: str) -> list[str]:
    clean_markdown = "\n".join([line.strip()
                               for line in markdown.splitlines()])
    return [block.strip() for block in clean_markdown.split("\n\n") if len(block) >= 1]
