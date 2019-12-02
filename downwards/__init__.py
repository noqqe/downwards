#!/usr/bin/env python3

import sys
import click
import wikipedia
import wikitextparser as wtp
from mako.template import Template


mandoc = '''
.Dd $Mdocdate: 30.11.2019 $
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
    article = wikipedia.page(name)

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


def render_article(article, language, template=mandoc):

    mdoc = Template(template)

    sections = flatten_content_hierarchy(article)

    rendered = mdoc.render(
            title=article.title,
            links=article.links,
            sections=sections,
            url=article.url,
            lang=language
            )

    print(rendered)


@click.command()
@click.option('--language', '-l', default='de', help='Language for wikipedia')
@click.argument('article')
def main(article, language):
    result = get_article(article, language)
    render_article(article=result, language=language, template=mandoc)


if __name__ == '__main__':
    main()
