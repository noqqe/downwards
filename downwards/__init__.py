#!/usr/bin/env python3

import sys
import tempfile
import subprocess
import click
import wikipedia
import wikitextparser as wtp
from mako.template import Template
import datetime


mandoc = '''
.Dd ${date} $
.Dt Wikipedia ${lang}
.Os
.Sh NAME
.Nm ${title}
.Nd ${url}
${sections}
.Ed
.Sh Links
.It
% for link in links:
.Xr ${link}
% endfor
'''


def get_article(name, language):

    if name is None:
        sys.exit(1)

    wikipedia.set_lang(language)

    try:
        article = wikipedia.page(name)
    except wikipedia.exceptions.PageError:
        print("Error: Page {} not found!".format(name))
        sys.exit(1)

    return article


def flatten_content_hierarchy(article):

    n = '\n'
    flt = ".Sh Zusammenfassung" + n + n

    sections = wtp.parse(article.content).sections

    for section in sections:
        if not section.title == "":
            flt = flt + ".Sh " + section.title + n + n
        sec = wtp.parse(section.contents).sections[0]
        flt = flt + sec.contents + n

    return flt


def render_article(article, language, template, date):

    mdoc = Template(template)

    sections = flatten_content_hierarchy(article)

    rendered = mdoc.render(
            title=article.title,
            links=article.links,
            sections=sections,
            url=article.url,
            lang=language,
            date=date,
            )

    return rendered

def man_wrapper(content):
    _, tmpfile = tempfile.mkstemp(prefix="man-", text=True, suffix=".1")
    with open(tmpfile, 'w') as f:
        f.write(content)

    subprocess.call(['man', tmpfile])

    return True

@click.command()
@click.option('--language', '-l', default='de', help='Language for wikipedia')
@click.option('--stdout', '-s', default=False, is_flag=True, help='Print to stdout')
@click.argument('article')
def main(article, language, stdout):
    result = get_article(article, language)
    rendered = render_article(article=result, language=language, template=mandoc, date=str(datetime.date.today()))

    if stdout:
        print(rendered)
    else:
        man_wrapper(rendered)


if __name__ == '__main__':
    main()
