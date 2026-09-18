from textnode import TextNode, TextType, text_node_to_html_node
import re
from htmlnode import HTMLNode, ParentNode, LeafNode

def split_nodes_delimiter(old_nodes: list[TextNode], delimiter: str, text_type: TextType) -> list[TextNode]:
    delimited_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            delimited_nodes.append(old_node)
        # delimiter_count = 0
        # for delimiter in old_node.text:
        #     delimiter_count++
        # if delimiter_count%2 != 0:
        #     raise Exception('Invalid Markdown syntax.')
        else:
            parts = old_node.text.split(delimiter)
            if len(parts) % 2 != 1:
                raise Exception('Invalid Markdown syntax.')
            for i in range (len(parts)):
                if parts[i] == '':
                    continue
                elif i % 2 == 1:
                    delimited_nodes.append(TextNode(parts[i], text_type))
                else:
                    delimited_nodes.append(TextNode(parts[i], TextType.TEXT))
    return delimited_nodes

def extract_markdown_images(text) -> list[tuple[str,str]]:
    return re.findall(r"!\[([^\[\]]*)\]\(([^\(\)]*)\)", text)
    # [!\[(.?*)\]]

def extract_markdown_links(text) -> list[tuple[str,str]]:
    return re.findall(r"(?<!!)\[([^\[\]]*)\]\(([^\(\)]*)\)", text)

def split_nodes_image(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue
        markdown_images = extract_markdown_images(old_node.text)
        # if markdown_images is None:
        #     return [old_node]
        if markdown_images == []:
            # return [old_node]
            split_nodes.append(old_node)
            continue
        split_text = old_node.text
        for split in markdown_images:
            split_text = split_text.split(f'![{split[0]}]({split[1]})', maxsplit=1)
            if split_text[0] == '':
                pass
            else:
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(split[0], TextType.IMAGE, split[1]))
            split_text = split_text[1]
        # for i in range(len(split_text)):
        #     if split_text[i] == '':
        #         pass
        #     elif i % 2 == 1:
        #         split_nodes.append(TextNode(markdown_images[i-1], TextType.IMAGE, markdown_links[i]))
        #     else:
        #         split_nodes.append(TextNode(split_text[i], TextType.TEXT))
        if split_text != '':
            split_nodes.append(TextNode(split_text, TextType.TEXT))
    return split_nodes


def split_nodes_link(old_nodes: list[TextNode]) -> list[TextNode]:
    split_nodes = []
    for old_node in old_nodes:
        if old_node.text_type != TextType.TEXT:
            split_nodes.append(old_node)
            continue
        markdown_links = extract_markdown_links(old_node.text)
        # if markdown_links is None:
        #     return [old_node]
        if markdown_links == []:
            split_nodes.append(old_node)
            continue
            # return [old_node]
        split_text = old_node.text
        for split in markdown_links:
            # print(repr(split_text))
            # print(f'[{split[0]}]({split[1]})')
            split_text = split_text.split(f'[{split[0]}]({split[1]})', maxsplit=1)
            if split_text[0] == '':
                pass
            else:
                split_nodes.append(TextNode(split_text[0], TextType.TEXT))
            split_nodes.append(TextNode(split[0], TextType.LINK, split[1]))
            split_text = split_text[1]
        if split_text != '':
            split_nodes.append(TextNode(split_text, TextType.TEXT))
    return split_nodes

def text_to_textnodes(text) -> list[TextNode]:
    nodes = [TextNode(text,TextType.TEXT)]
    nodes = split_nodes_delimiter(nodes, '**', TextType.BOLD)
    nodes = split_nodes_delimiter(nodes, '_', TextType.ITALIC)
    nodes = split_nodes_delimiter(nodes, '`', TextType.CODE)
    nodes = split_nodes_image(nodes)
    nodes = split_nodes_link(nodes)
    return nodes

def text_to_children(text) -> list[LeafNode]:
    nodes = text_to_textnodes(text)
    child_nodes = []
    for node in nodes:
        child_nodes.append(text_node_to_html_node(node))
    return child_nodes

def extract_title(markdown):
    lines = markdown.split('\n')
    for line in lines:
       if line.startswith('# '):
           header = line[2:].strip()
           return header
    raise Exception('There is no h1 header.')
