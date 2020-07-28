#!/usr/bin/env python3

"""
A class-based system for rendering html.
"""


# This is the framework for the base class
class Element(object):

    tag = "html"

    def __init__(self, content=None, **kwargs):
        if content is None:
            self.contents = []
        else:
            self.contents = [content]
        self.attribute = kwargs

    def append(self, new_content):
        self.contents.append(new_content)

    def _open_tag(self):
        if self.attribute:
            open_tag = ["<{} ".format(self.tag)]
            for key, value in self.attribute.items():
                open_tag.append(f'{key}="{value}" ')    # make sure "" on the {value}, add space after {value}
            open_tag[-1] = open_tag[-1][:-1]    #  remove last space
            open_tag.append(">")
            return "".join(open_tag)
        else:
            return "<{}>".format(self.tag)

    def _close_tag(self):
        return "</{}>".format(self.tag)

    def render(self, out_file):

        out_file.write(self._open_tag())
        out_file.write("\n")
        for content in self.contents:
            try:
                content.render(out_file)
            except AttributeError:
                out_file.write(content)
                out_file.write("\n")
        out_file.write(self._close_tag())
        out_file.write("\n")


class Html(Element):

    tag = "html"


class Body(Element):

    tag = "body"


class P(Element):

    tag = "p"


class Head(Element):

    tag = "head"


class OneLineTag(Element):

    def render(self, out_file):
        out_file.write("<{}>".format(self.tag))
        out_file.write(self.contents[0])
        out_file.write("</{}>\n".format(self.tag))

    def append(self, content):
        raise NotImplementedError


class Title(OneLineTag):

    tag = "title"


class SelfClosingTag(Element):

    def render(self, out_file):
        tag = self._open_tag()[:-1] + " />\n"   #  need a space before />
        out_file.write(tag)


class Hr(SelfClosingTag):

    tag = "hr"


class Br(SelfClosingTag):

    tag = "br"

    def __init__(self, content=None, **kwargs):
        if content is not None:
            raise TypeError("SelfClosingTag can not contain any content")
        super().__init__(content, **kwargs)

    def append(self, *args):
        raise TypeError("You can not add content to a SelfClosingTag")
