from typing_extensions import Optional
from typing_extensions import Optional, Sequence


class HTMLNode:
    def __init__(
        self,
        tag: Optional[str] = None,
        value: Optional[str] = None,
        children: Optional[Sequence["HTMLNode"]] = None,
        props: Optional[dict[str, str]] = None,
    ):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        result = ""
        if self.props is not None:
            for prop in self.props:
                result += f' {prop}="{self.props[prop]}"'
        return result

    def __repr__(self) -> str:
        return f"HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})"
