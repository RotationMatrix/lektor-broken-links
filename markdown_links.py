import mistune
import sys


class LinkScraper(mistune.Renderer):
    def __init__(self):
        super().__init__()
        self.links = []

    def link(self, link, title=None, text=None):
        self.links.append(link)


def find_links(text: str):
    renderer = LinkScraper()
    markdown = mistune.Markdown(renderer)
    markdown(text)

    return renderer.links
