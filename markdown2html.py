#!/usr/bin/python3
"""Markdown 2 HTML"""
from sys import argv, stderr
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
    def tag(line):
        tags = {'open': {'#': '<h{}>', '-': '<ul>', '*': '<ol>'},
                'closed': {'__': '<em>', '**': '<b>', '[[{}]]': '{}'}}
        fmted = line
        md_char_count = {'__': (int(line.count('__') / 2)),
                         '**': (int(line.count('**') / 2)), 
                         '[[': (int(line.count('[[') / 2))}
        print(md_char_count)
        for char in md_char_count.keys():
            for times in range(md_char_count[char]):
                otag = tags['closed'][char]
                ctag = otag[0] + '/' + otag[1:]
                fmted = fmted.replace(char, otag, 1)
                fmted = fmted.replace(char, ctag, 1)
        print(fmted)
        return fmted

    with open(md, 'r') as md_file:
        md_content = md_file.readlines()

        htmled, li_tags, md_chars = [], [], []
        tags = {'open': {'#': '<h{}>', '-': '<ul>', '*': '<ol>'},
                'closed': {'__': '<em>', '**': '<b>', '[[{}]]': '{}'}}

        for index in range(len(md_content)):
            line = md_content[index]
            md_char = line.split(' ')[0]

            if '#' in md_char:
                text = line[len(md_char)+1:-1]
                heading = '<h{}>{}</h{}>'.format(len(md_char), text, len(md_char))
                htmled += [heading]

            elif md_char[0] in ['-', '*']:
                otag = tags['open'][md_char]
                ctag = otag[0] + '/' + otag[1:]
                text = line[2:-1]
                li = '\t<li>' + tag(text) + '</li>'
                li_tags += [li]

                if index + 1 == len(md_content) or md_content[index + 1][0] not in ['-', '*']:
                    list_html = [otag] + li_tags + [ctag]
                    htmled += list_html
                    li_tags = []
            else:
                if len(line) > 0:
                    text = tag(line)
                    p = '<p>{}</p>'.format(text)
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
