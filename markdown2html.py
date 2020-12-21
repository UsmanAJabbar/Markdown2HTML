#!/usr/bin/python3
"""Markdown 2 HTML"""
from sys import argv, stderr
import os
tags = {'open': {'#': '<h{}>', '-': '<ul>', '*': '<ol>'},
        'closed': {'__': '<em>', '**': '<b>', '[[': '{}'}}


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
    with open(md_file, 'r') as md_file:
        md_content = md_file.readlines()

        htmled, li_tags = [], []

        for index in range(len(md_content)):
            line = md_content[index]
            md_char = line.split(' ')[0]
            md_char = md_char if md_char[-1] != '\n' else md_char[-1]

            if '#' in md_char:
                text = line[len(md_char)+1:-1]
                heading = '<h{}>{}</h{}>'.format(len(md_char), text, len(md_char))
                htmled += [heading]

            elif md_char == '*' or md_char == '-':
                otag = tags['open'][md_char]
                ctag = otag[0] + '/' + otag[1:]
                text = line[2:-1]
                li = '\t<li>' + formatter(text) + '</li>'
                li_tags += [li]

                if index + 1 == len(md_content) or md_content[index + 1][0] not in ['-', '*']:
                    list_html = [otag] + li_tags + [ctag]
                    htmled += list_html
                    li_tags = []
            else:
                if len(line) > 1:
                    text = formatter(line)
                    p = '<p>{}</p>'.format(text)
                    htmled += [p]

        with open(html_file, 'w') as html_file:
            for strings in htmled:
                html_file.writelines(strings + '\n')

def formatter(text):
    """
    -----------------
    HELPER: formatter
    -----------------
    Description:
        Helper function that adds and replaces
        the necessary format tags regardless of
        how many times they may occur on a single
        line.
    Args:
        @text: input string with GitHub-like markdown
    """
    fmted = text
    md_char_count = {'__': (int(text.count('__') / 2)),
                     '**': (int(text.count('**') / 2)),
                     '[[': (int(text.count('[[') / 2))}
    for char in md_char_count.keys():
        for times in range(md_char_count[char]):
            otag = tags['closed'][char]
            ctag = otag[0] + '/' + otag[1:]
            fmted = fmted.replace(char, otag, 1)
            fmted = fmted.replace(char, ctag, 1)
    return fmted

if __name__ == "__main__":
    if len(argv) != 3:
        stderr.write('Usage: ./markdown2html.py README.md README.html' + '\n')
        exit(1)

    md, html = argv[1], argv[2]

    if not os.path.isfile(md):
        stderr.write('Missing {}'.format(md + '\n'))
        exit(1)

    md_to_html(md, html)
    exit(0)
