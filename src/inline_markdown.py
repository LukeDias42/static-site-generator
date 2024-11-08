import re
from textnode import TextNode, TextType


def text_to_textnodes(text: str) -> list[TextNode]:
    main_node = TextNode(text, TextType.TEXT)
    return split_nodes_link(
        split_nodes_image(
            split_nodes_delimiter(
                split_nodes_delimiter(
                    split_nodes_delimiter([main_node], "**", TextType.BOLD),
                    "*",
                    TextType.ITALIC,
                ),
                "`",
                TextType.CODE,
            )
        )
    )


def split_nodes_delimiter(
    old_nodes: list[TextNode], delimiter: str, text_type: TextType
) -> list[TextNode]:
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        sections = old_node.text.split(delimiter)
        if len(sections) % 2 == 0:
            raise ValueError("Incorrectly formatted type.")
        split_nodes = []
        for i in range(len(sections)):
            if sections[i] == "":
                continue
            if i % 2 == 0:
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            else:
                split_nodes.append(TextNode(sections[i], text_type))
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    image_regex = r"\!\[.*?\]\(.*?\)"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        sections = re.split(image_regex, old_node.text)
        split_nodes = []
        images_data = extract_markdown_images(old_node.text)
        for i in range(len(sections)):
            if sections[i] != "":
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i < len(sections) - 1:
                split_nodes.append(
                    TextNode(images_data[i][0],
                             TextType.IMAGE, images_data[i][1])
                )
        new_nodes.extend(split_nodes)
    return new_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    link_regex = r"(?<!!)\[.*?\]\(.*?\)"
    new_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT.value:
            new_nodes.append(old_node)
            continue
        sections = re.split(link_regex, old_node.text)
        split_nodes = []
        link_data = extract_markdown_links(old_node.text)
        for i in range(len(sections)):
            if sections[i] != "":
                split_nodes.append(TextNode(sections[i], TextType.TEXT))
            if i < len(sections) - 1:
                split_nodes.append(
                    TextNode(link_data[i][0], TextType.LINK, link_data[i][1])
                )
        new_nodes.extend(split_nodes)
    return new_nodes


def extract_markdown_images(text: str) -> list[str]:
    image_regex = r"\!\[(.*?)\]\((.*?)\)"
    result = re.findall(image_regex, text)
    return result


def extract_markdown_links(text: str) -> list[str]:
    link_regex = r"(?<!!)\[(.*?)\]\((.*?)\)"
    result = re.findall(link_regex, text)
    return result
