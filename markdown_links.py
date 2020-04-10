from markdown_it import MarkdownIt
import sys

def find_links(text: str):
    md = MarkdownIt()
    tokens = md.parse(text)

    # Conduct a breadth-first search for 'link_open' tokens.
    links = []
    stack = tokens
    while len(stack) > 0:
        # Copy the stack to a working stack and prep for the next loop.
        current_stack = stack.copy()
        stack.clear()

        for token in current_stack:
            # Capture any link destinations.
            if token.type == 'link_open':
                links.append(token.attrs[0][1])

            # Add any children to the stack for the next loop.
            if token.children != None:
                stack.extend(token.children)

    return links
