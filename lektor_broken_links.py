# -*- coding: utf-8 -*-
from furl import furl
from click import style
from lektor.pluginsystem import Plugin
from lektor.db import Page
from time import time
import mistune
import os
import re
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


class BrokenLinksPlugin(Plugin):
    name = 'Broken Links'
    description = u'Find all the broken links in your Lektor site!'

    def on_before_build_all(self, builder, **extra):
        self.sources = []
        self.paths = []

    def on_before_build(self, source, prog, **extra):
        if type(source) is Page:
            if os.path.exists(source.source_filename):
                if source not in self.sources:
                    self.sources.append(source)

                if source.url_path not in self.paths:
                    self.paths.append(source.url_path)

    def on_after_build_all(self, **extra):
        print(style("Started link check", fg='cyan'))
        start_time = time()

        for source in self.sources:
            broken_links = self.get_broken_links(source)
            num_links = len(broken_links)

            if num_links > 0:
                link = 'links'
                if num_links == 1:
                    link = 'link'

                print(style("Found %i broken %s in '%s':" %
                            (num_links, link, source.path), fg='red'))

                for link in broken_links:
                    print("    " + link)

        duration = time() - start_time
        print(style("Finished link check in %.2f sec" % duration, fg='cyan'))

    def get_broken_links(self, source):
        broken_links = []
        with open(source.source_filename) as f:
            links = find_links(f.read())

        for link in links:
            # Find internal links
            if re.match(r'\.{0,2}/.*', link):
                if furl(link).path.isabsolute:
                    dest = furl('/')
                else:
                    dest = furl(source.path)

                dest.path = (dest.path / link / '/').normalize()
                dest = furl('/').join(dest)

                if str(dest) not in self.paths:
                    broken_links.append(link)

                # print(link, '->', dest)

        return broken_links
