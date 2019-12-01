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
% for section in sections:
    % if loop.index == 0:
.Sh Zusammenfassung
    % else:
.Sh ${section.title}
    % endif
${section.contents}
% endfor
.Ed
.Sh Links
.It
% for link in links:
.Xr ${link}
% endfor
'''


def get_article(name, language="de"):

    if name is None:
        sys.exit(1)

    wikipedia.set_lang(language)
    article = wikipedia.page(name)

    return article


def render_article(article, language, template=mandoc):

    mdoc = Template(template)

    sections = wtp.parse(article.content).sections

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
    result = get_article(article)
    render_article(article=result, language=language, template=mandoc)

if __name__ == '__main__':
    main()
