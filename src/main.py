import shutil

from textnode import TextNode
from textnode import TextType
import os
from block_markdown import markdown_to_html_node
from inline_markdown import extract_title

#./main.sh
# print('hello world')
#
def cleanup(destination):
    if os.path.exists(destination):
        shutil.rmtree(destination)
        os.mkdir(destination)
    else:
        os.mkdir(destination)

def copy_directory(source, destination):
    copy_log = []
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isdir(item_path):
            if not os.path.exists(dest_path):
                copied_dir = os.mkdir(dest_path)
                copy_log.append(copied_dir)
            copy_log.extend(copy_directory(item_path, dest_path))
        else:
            copied = shutil.copy(item_path, dest_path)
            copy_log.append(copied)
    return(copy_log)

def generate_page(from_path, template_path, dest_path):
    print(f'Generating page from {from_path} to {dest_path} using {template_path}.')
    with open(from_path) as file:
        from_file = file.read()
    with open(template_path) as file:
        template_file = file.read()
    node = markdown_to_html_node(from_file)
    html = node.to_html()
    title = extract_title(from_file)
    # html.replace(title, '')
    template_file = template_file.replace('{{ Title }}', title)
    template_file = template_file.replace('{{ Content }}', html)
    if not os.path.exists(os.path.dirname(dest_path)):
        os.makedirs(os.path.dirname(dest_path))
    # with open(template_file) as file:
        # with open(f'{dest_path}/{title}') as writer:
    with open(dest_path, 'w') as writer:
        writer.write(template_file)

def generate_pages(source, template, destination):
    pages_generated = []
    for item in os.listdir(source):
        item_path = os.path.join(source, item)
        dest_path = os.path.join(destination, item)
        if os.path.isdir(item_path):
            if not os.path.exists(os.path.dirname(dest_path)):
                os.makedirs(os.path.dirname(dest_path))
            generate_pages(item_path, 'template.html', dest_path)
            # pages_generated.extend(generate_pages(item_path, 'template.html', dest_path))
        else:
            if item[-3:] == '.md':
                generate_page(item_path, 'template.html', f'{dest_path[:-3]}.html')
                pages_generated.append(f'{dest_path[:-3]}.html' + ' generated from ' + item_path)
    print(pages_generated)
    # return(pages_generated)

def main():
    # node = TextNode('This is some anchor text', TextType.LINK, 'https://www.boot.dev')
    # print(node)
    cleanup('./public')
    print(copy_directory('./static', './public'))
    print(copy_directory('./content', './public'))
    generate_pages('content/', 'template.html', 'public/')
    # print(generate_pages('content/', 'template.html', 'public/'))

main()
