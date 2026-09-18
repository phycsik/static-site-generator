class HTMLNode:

    def __init__(self,
        tag: str | None = None,
        value: str | None = None,
        children: list[HTMLNode] | None = None,
        props: dict[str,str] | None = None):
        self.tag = tag
        self.value = value
        self.children = children
        self.props = props

    def to_html(self):
        raise NotImplementedError

    def props_to_html(self):
        if not self.props:
           return ''
        props_dict = f''
        for key in self.props:
            props_dict += f' {key}="{self.props[key]}"'
        return props_dict

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class ParentNode(HTMLNode):

    def __init__(self,
        tag,
        children,
        props: dict[str,str] | None = None):
        super().__init__(tag=tag, children=children, props=props)


    def to_html(self):
        if not self.tag:
            raise ValueError
        if self.children is None:
            raise ValueError
        html_string = ''
        for child in self.children:
            html_string += child.to_html()
        html_string = f'<{self.tag}{super().props_to_html()}>{html_string}</{self.tag}>'
        return html_string

    def props_to_html(self):
        if not self.props:
           return ''
        props_dict = f''
        for key in self.props:
            props_dict += f' {key}="{self.props[key]}"'
        return props_dict

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.children == other.children and self.props == other.props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.children}, {self.props})'

class LeafNode(HTMLNode):

    def __init__(self,
        tag,
        value,
        props: dict[str,str] | None = None):
        # self.tag = tag
        # self.value = value
        # self.props = props
        super().__init__(tag=tag, value=value, props=props)

    def __eq__(self, other):
        return self.tag == other.tag and self.value == other.value and self.props == other.props

    def __repr__(self):
        return f'HTMLNode({self.tag}, {self.value}, {self.props})'

    def to_html(self):
        if self.value is None:
            # raise ValueError(f"leaf node has no value: {self}")
            raise ValueError
        if self.tag == None:
            return f'{self.value}'
        html_string = f'<{self.tag}{super().props_to_html()}>{self.value}</{self.tag}>'
        return html_string
