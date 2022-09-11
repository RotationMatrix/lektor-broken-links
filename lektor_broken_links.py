# -*- coding: utf-8 -*-
from furl import furl
from click import style
from lektor.pluginsystem import Plugin
from lektor.db import Page
from time import time
import mistune
import os
import re


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


class BrokenLinksPlugin(Plugin):
    name = "Broken Links"
    description = "Find all the broken links in your Lektor site!"

    def __init__(self, env, plugin_id):
        super().__init__(env, plugin_id)
        self.sources = []
        self.paths = []

    def on_before_build_all(self, builder, **extra):
        self.sources = []
        self.paths = []

    def on_before_build(self, source, prog, **extra):
        if isinstance(source, Page):
            if os.path.exists(source.source_filename):
                if source not in self.sources:
                    self.sources.append(source)

                if source.url_path not in self.paths:
                    self.paths.append(source.url_path)

    def on_after_build_all(self, **extra):
        print(style("Started link check", fg="cyan"))
        start_time = time()

        for source in self.sources:
            broken_links = self.get_broken_links(source)
            num_links = len(broken_links)

            if num_links > 0:
                link = "links"
                if num_links == 1:
                    link = "link"

                print(
                    style(f"Found {num_links} broken {link} in '{source.path}':", fg="red"))

                for link in broken_links:
                    print("    " + link)

        duration = time() - start_time
        print(style(f"Finished link check in {duration:.2} sec", fg="cyan"))

    def get_broken_links(self, source):
        broken_links = []
        with open(source.source_filename, encoding="utf-8") as f:
            links = find_links(f.read())

        for link in links:
            # Find internal links (i.e. anything without a protocol://)
            if re.match(r"^([^:]|:(?!//))+$", link):
                if furl(link).path.isabsolute:
                    dest = furl("/")
                else:
                    dest = furl(source.path)

                dest.path = (dest.path / link / "/").normalize()
                dest = furl("/").join(dest)

                if str(dest) not in self.paths:
                    broken_links.append(link)

        return broken_links
