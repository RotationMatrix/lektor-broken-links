# -*- coding: utf-8 -*-
from furl import furl
from click import style
from lektor.pluginsystem import Plugin
from lektor.project import Project
from lektor.db import Page
from markdown_links import find_links
import re
import os


class BrokenLinksPlugin(Plugin):
    name = 'Broken Links'
    description = u'Add your description here.'
    broken_links = {}

    def on_before_build(self, source, prog, **extras):
        def check(canonical_link: str, original_link: str):
            pad = Project.discover().make_env().new_pad()

            if pad.resolve_url_path(canonical_link, include_assets=False) is None:
                if source not in self.broken_links:
                    self.broken_links[source] = []

                if original_link not in self.broken_links[source]:
                    self.broken_links[source].append(original_link)

        if type(source) is Page:
            if os.path.exists(source.source_filename):
                file = open(source.source_filename)
                text = file.read()
                file.close()
                links = find_links(text)

                internal_links = []
                for link in links:
                    # Find internal links
                    if re.match(r'\.{0,2}/.*', link):
                        if furl(link).path.isabsolute:
                            dest = furl('/')
                        else:
                            dest = furl(source.path)

                        dest.path = (dest.path / link).normalize()
                        dest = furl('/').join(dest)
                        internal_links.append((str(dest), link))

                        # print(link, '->', dest)

                del links

                for link in internal_links:
                    check(link[0], link[1])

    def on_after_build_all(self, **extras):
        for key in self.broken_links.keys():
            num_links = len(self.broken_links[key])
            link = 'links'

            if num_links == 1:
                link = 'link'

            print(style("Found %i broken %s in '%s':" %
                        (num_links, link, key.path), fg='red'))

            for link in self.broken_links[key]:
                print("    " + link)

        # Clear the dict so it doesn't show up on the next build.
        self.broken_links.clear()
