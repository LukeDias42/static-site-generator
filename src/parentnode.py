from htmlnode import HTMLNode


class ParentNode(HTMLNode):
    def __init__(self, tag, children, props=None):
        super().__init__(tag, None, children, props)

    def to_html(self) -> str:
        if self.tag is None:
            raise ValueError("Parent Node needs a tag to be parsed.")
        if self.children is None:
            raise ValueError("Parent Node needs children to be parsed.")
        result = f"<{self.tag}{self.props_to_html()}>"
        for child in self.children:
            result += f"{child.to_html()}"
        result += f"</{self.tag}>"
        return result
