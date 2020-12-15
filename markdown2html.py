#!/usr/bin/python3
"""Markdown 2 HTML"""
from sys import argv
from sys import stderr
import os

def md_to_html(md_file, html_file):
    """
    ------------------
    METHOD: md_to_html
    ------------------
    Description:
        Method that converts markdown content
        to HTML
    ARGS:
        @md_file: input markdown file name
        @html_file: output HTML file name
    """
    with open(md, 'r') as md_file:
        md_content = md_file.readlines()

        htmled = []
        md_chars = ['#', '-', '*', '**', '__', '[[' ']]', '((', '))']

        for line in md_content:
            if line[0] in md_chars:
                md_char = line[0]
                md_char_count = 0
                md_area = line[0:5] if len(line) > 5 else line

                if md_char in md_chars:
                    for chars in md_area:
                        md_char_count += 1 if chars == md_char else 0
                    if md_char == '#':
                        text = line.replace('#', '')[1:-1]
                        heading = '<h{}>{}</h{}>'.format(md_char_count, text, md_char_count)
                        htmled += [heading]
                else:
                    if len(line) > 0:
                        p = '<p>{}</p>'.format(line)
                        htmled += [p]

        with open(html, 'w') as html_file:
            for strings in htmled:
                html_file.writelines(strings + '\n')

if __name__ == "__main__":
    if len(argv) < 2:
        stderr.write('Usage: ./markdown2html.py README.md README.html')
        exit(1)

    md, html = argv[1], argv[2]

    if not os.path.isfile(md):
        stderr.write('Missing {}'.format(md))
        exit(1)

    md_to_html(md, html)
