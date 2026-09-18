from enum import Enum
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import text_to_children
from textnode import TextNode, text_node_to_html_node, TextType

class BlockType(Enum):
    PARAGRAPH = 'paragraph'
    HEADING = 'heading'
    CODE = 'code'
    QUOTE = 'quote'
    UNORDERED_LIST = 'unordered list'
    ORDERED_LIST = 'ordered list'

def markdown_to_blocks(markdown) -> list(str):
    blocks = markdown.split('\n\n')
    blocks_stripped = []
    for block in blocks:
        block = block.strip()
        if block == '':
            # del block
            continue
        blocks_stripped.append(block)
    return blocks_stripped


def block_to_block_type(block) -> BlockType:
    # for i in range(len(block)):
        # block[:6] contains
    if block.startswith('```\n') and block.endswith('```'):
        return BlockType.CODE
    lines = block.split('\n')
    for line in lines:
        if line.startswith('#'):
            for i in range(1, 7):
                heading_count = '#' * i
                if line.startswith(heading_count + ' '):
                    return BlockType.HEADING
        if line.startswith('>'):
            return BlockType.QUOTE
        if line.startswith('- '):
            return BlockType.UNORDERED_LIST
        if line.startswith('1. '):
            # for i, line in range(1, len(lines[line:]))
            #     if lines[+i].startswith(f'{1 + i}. ')
            #         return BlockType.ORDERED_LIST
            for i, line in enumerate(lines):
                if line.startswith(f'{1 + i}. '):
                    if i == (len(lines)-1):
                        return BlockType.ORDERED_LIST
                    continue
                else:
                    break
        return BlockType.PARAGRAPH
        # if block[i] == '#' and block[i+1:i+3] == ' \n':
        #         return BlockType.HEADING
        # if block[i:i+2] == '`' and block[i+3:i+4]

def markdown_to_html_node(markdown) -> ParentNode:
    blocks = markdown_to_blocks(markdown)
    div_children = []
    for block in blocks:
        block_type = block_to_block_type(block)
        lines = block.split('\n')
        match block_type:
            case BlockType.HEADING:
                hash_count = number_hashes_helper(block)
                heading_text = block[hash_count + 1:]
                child_nodes = text_to_children(heading_text)
                heading_node = ParentNode(f'h{hash_count}', children=child_nodes)
                div_children.append(heading_node)
            case BlockType.QUOTE:
                # quote_text = ''
                quote_list = []
                for line in lines:
                    if line.startswith('> '):
                        quote_list.append(line[2:])
                    elif line[0] == '>':
                        quote_list.append(line[1:])
                quote_text = ' '.join(quote_list)
                child_nodes = text_to_children(quote_text)
                quote_node = ParentNode('blockquote', children=child_nodes)
                div_children.append(quote_node)
            case BlockType.UNORDERED_LIST:
                # ulist_list = []
                # for line in lines:
                #     ulist_list.append(line[2:])
                # ulist_text = ' '.join(ulist_list)
                # child_nodes = text_to_children(ulist_text)
                # ulist_node = HTMLNode('ul', children=child_nodes)
                # div_children.append(ulist_node)
                li_nodes = []
                for line in lines:
                    inline_children = text_to_children(line[2:])
                    li_node = ParentNode('li', children=inline_children)
                    li_nodes.append(li_node)
                ulist_node = ParentNode('ul', children=li_nodes)
                div_children.append(ulist_node)
            case BlockType.ORDERED_LIST:
                li_nodes = []
                for line in lines:
                    inline_children = text_to_children(line[2:].strip())
                    li_node = ParentNode('li', children=inline_children)
                    li_nodes.append(li_node)
                olist_node = ParentNode('ol', children=li_nodes)
                div_children.append(olist_node)
            case BlockType.CODE:
                # print(repr(block))
                code_list = []
                for line in lines:
                    code_list.append(line.strip())
                stripped_code_text = "\n".join(code_list)
                # text = block[4:-3]
                code_textnode = TextNode(stripped_code_text[4:-3], TextType.CODE)
                code_htmlnode = [text_node_to_html_node(code_textnode)]
                # code_block = [ParentNode('code', children=code_htmlnode)]
                code_block_pre = ParentNode('pre', children=code_htmlnode)
                div_children.append(code_block_pre)
            case BlockType.PARAGRAPH:
                # paragraph_list = []
                paragraph_text = " ".join(line.strip() for line in lines)
                # for line in lines:
                #     paragraph_list.append(line)
                # paragraph_text = " ".join(paragraph_list)
                # print(text_to_children(paragraph_text))
                paragraph_children = text_to_children(paragraph_text)
                paragraph_node = ParentNode('p', children = paragraph_children)
                div_children.append(paragraph_node)
    div = ParentNode('div', div_children)
    return div

def number_hashes_helper(block) -> int:
    lines = block.split('\n')
    for line in lines:
        if line.startswith('#'):
            for i in range(1, 7):
                heading_count = '#' * i
                if line.startswith(heading_count + ' '):
                    return i
