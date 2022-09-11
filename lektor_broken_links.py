# -*- coding: utf-8 -*-
from furl import furl
from click import style
from lektor.pluginsystem import Plugin
from lektor.db import Page
from time import time
import mistune
import os
import re
import urllib


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


def prompt_external_links():
    selection = " "
    # Repeat until the user enters a new line, Y or N.
    while not re.fullmatch(r"([YyNn].*)?", selection):
        print("Check for broken external links?")
        selection = input(
            "This will make HTTP requests to links in this project. [Y/n]: ")

    # Check external links unless the user instructs us not to.
    if not re.match(r"[Nn].*", selection):
        return True
    else:
        return False


class BrokenLinksPlugin(Plugin):
    name = "Broken Links"
    description = "Find all the broken links in your Lektor site!"

    def __init__(self, env, plugin_id):
        super().__init__(env, plugin_id)
        self.sources = []
        self.paths = []

        self.check_external_links = False
        try:
            if os.environ["CHECK_EXT_LINKS"] == "1":
                self.check_external_links = True
            elif os.environ["CHECK_EXT_LINKS"] == "ask":
                self.check_external_links = prompt_external_links()
        except KeyError:
            self.check_external_links = False

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
                    if link[1] is None and link[2] is None:
                        print('    ' + link[0])
                    else:
                        print(
                            '    ' + link[0] + ' ' + '(HTTP ' + str(link[1]) + ' ' + link[2] + ')')

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
                    broken_links.append([link, None, None])

            # Find external HTTP links.
            elif self.check_external_links and re.match(r'https?://.*', link):
                status_code = 0
                status_reason = ''

                try:
                    with urllib.request.urlopen(link) as response:
                        status_code = response.status
                        status_reason = response.reason
                except urllib.error.HTTPError as error:
                    status_code = error.code
                    status_reason = error.reason

                if status_code != 200:
                    broken_links.append([link, status_code, status_reason])

        return broken_links
