import unittest
from htmlnode import HTMLNode, LeafNode, ParentNode
from inline_markdown import extract_markdown_images, extract_markdown_links


class TestHTMLNode(unittest.TestCase):
    def test_eq(self):
        node = HTMLNode('"p"', '"This is an HTMLNode."')
        node2 = HTMLNode('"p"', '"This is an HTMLNode."')
        self.assertEqual(node, node2)

    def test_props(self):
        node = HTMLNode('"p"', '"This is an HTMLNode."', props = {"href": "www.boot.dev"})
        self.assertEqual(node.props_to_html(), ' href="www.boot.dev"')
        # assert node.props_to_html() is not None
        # return unittest.FunctionTestCase(node.test_props)

    def test_repr(self):
        node = HTMLNode("p", "This is an HTMLNode.", [HTMLNode()], {"href": "www.boot.dev"})
        self.assertEqual(repr(node), "HTMLNode(p, This is an HTMLNode., [HTMLNode(None, None, None, None)], {'href': 'www.boot.dev'})")

    def test_leaf_to_html_p(self):
        node = LeafNode("p", "Hello, world!", {'leaf': 'test'})
        self.assertEqual(node.to_html(), '<p leaf="test">Hello, world!</p>')

    def test_to_html_with_children(self):
        child_node = LeafNode("span", "child")
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(parent_node.to_html(), "<div><span>child</span></div>")

    def test_to_html_with_grandchildren(self):
        grandchild_node = LeafNode("b", "grandchild")
        child_node = ParentNode("span", [grandchild_node])
        parent_node = ParentNode("div", [child_node])
        self.assertEqual(
            parent_node.to_html(), "<div><span><b>grandchild</b></span></div>")

    # def test_extract_markdown_images(self):
    #     text = "This is text with a ![rick roll](https://i.imgur.com/aKaOqIh.gif) and ![obi wan](https://i.imgur.com/fJRm4Vk.jpeg)"
    #     extracted_text = extract_markdown_images(text)
    #     self.assertEqual(extracted_text, [("rick roll", "https://i.imgur.com/aKaOqIh.gif"), ("obi wan", "https://i.imgur.com/fJRm4Vk.jpeg")])

    def test_extract_markdown_links(self):
        text = "This is text with a link [to boot dev](https://www.boot.dev) and [to youtube](https://www.youtube.com/@bootdotdev)"
        extracted_text = extract_markdown_links(text)
        self.assertEqual(extracted_text, [("to boot dev", "https://www.boot.dev"), ("to youtube", "https://www.youtube.com/@bootdotdev")])

    def test_extract_markdown_images(self):
        matches = extract_markdown_images(
            "This is text with an ![image](https://i.imgur.com/zjjcJKZ.png)"
        )
        self.assertListEqual([("image", "https://i.imgur.com/zjjcJKZ.png")], matches)

if __name__ == "__main__":
    unittest.main()
