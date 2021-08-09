#!/usr/bin/env python3
# -*- coding: utf-8 -*-

import sys
import tempfile
import subprocess
import unidecode
import datetime
import click
import wikipedia
import wikitextparser as wtp
from mako.template import Template


mandoc = '''.Dd ${date} $
.Dt Wikipedia ${lang}
.Os
.Sh NAME
.Nm ${title}
.Nd ${url}
${content}
.Sh Links
.Bl -column LOCAL -compact
% for link in links:
.It Li ${link}
% endfor
.El
'''


def get_article(name, language):
    """
    Fetches wikipedia article using its api and returns an
    Wikipedia Article object

    :name: str
    :language: str
    :returns: wikipedia.article()
    """

    if name is None:
        sys.exit(1)

    wikipedia.set_lang(language)

    try:
        article = wikipedia.page(name)
    except wikipedia.exceptions.PageError:
        print("Error: Page {} not found!".format(name))
        sys.exit(1)
    except wikipedia.exceptions.DisambiguationError as e:
        print("Error: Page {} is disambigous!".format(name))
        print("{}".format(e))
        sys.exit(1)

    return article


def umlaut_conversion(content):
    """
    Converts umlauts to ascii compatible characters
    :returns: str
    """

    flt = content

    # remove german umlauts
    flt = flt.replace('ä', 'ae')
    flt = flt.replace('ö', 'oe')
    flt = flt.replace('ü', 'ue')
    flt = flt.replace('ß', 'ss')
    flt = flt.replace('Ä', 'Ae')
    flt = flt.replace('Ü', 'Ue')
    flt = flt.replace('Ö', 'Oe')

    # remove unicode chars that man(1) does not understand
    flt = unidecode.unidecode(flt)

    return flt


def remove_multiple_newlines(content):
    """
    mdoc format gives a warning if multiple newlines are put
    into a document.

    To suppress this warning, we strip multiple newlines

    :returns: str
    """
    flt = content

    # remove double newlines
    flt = flt.replace('\n\n\n\n', '\n')
    flt = flt.replace('\n\n\n', '\n')
    flt = flt.replace('\n\n', '\n')

    return flt

def flatten_content_hierarchy(article, language='en'):
    """
    mdoc only knows about 1 layer of headlines (.Sh)
    In this function we convert

    = h1 =
    == h2 ==
    === h3 ==

    to

    .Sh h1
    .Sh h2
    .Sh h3

    which is a little strange because every Section() containes
    all subsections (h2) followed by the next Section(h2). We take
    each 1 section element from each object to strip down all content
    to mdoc

    :returns: str
    """
    n = '\n'

    if language == "de":
        flt = ".Sh Zusammenfassung" + n
    else:
        flt = ".Sh Summary" + n

    sections = wtp.parse(article.content).sections

    for section in sections:

        # grab first section of subsection (see func description)
        sec = wtp.parse(section.contents).sections[0]

        # Only add non-empty sections
        if len(sec.contents) > 0:
            if section.title is not None:
                flt = flt + ".Sh " + str(section.title) + n
            flt = flt + sec.contents + n

    return flt


def render_article(article, language, template, date):
    """
    Read the fetched content the convert it in multile ways to be read in
    man using mdoc format

    :article: str
    :language: str
    :template: mako.Template()
    :date: str following YYYY-MM-DD
    :returns: str (mdoc)
    """

    mdoc = Template(template)

    content = flatten_content_hierarchy(article=article, language=language)
    content = remove_multiple_newlines(content)
    content = umlaut_conversion(content)

    title = umlaut_conversion(article.title)

    rendered = mdoc.render(
            title=title,
            links=article.links,
            content=content,
            url=article.url,
            lang=language,
            date=date,
            )

    return rendered


def man_wrapper(content):
    """
    Writes str content to file and opens `man' command with the generated
    file as argument
    :returns: bool
    """
    _, tmpfile = tempfile.mkstemp(prefix="man-", text=True, suffix=".1")
    with open(tmpfile, 'w') as f:
        f.write(content)

    try:
        subprocess.call(['man', tmpfile])
    except:
        print("Could not open `man'. Path error?")
        sys.exit(1)

    return True


@click.command()
@click.option('--language', '-l', default='de', help='Language for wikipedia')
@click.option('--stdout', '-s', default=False, is_flag=True, help='Print to stdout')
@click.argument('article')
def main(article, language, stdout):
    """
    downwards lets you read a wikipedia page on command line as a manpage.

    """

    result = get_article(article, language)
    rendered = render_article(article=result, language=language, template=mandoc, date=str(datetime.date.today()))

    if stdout:
        print(rendered)
    else:
        man_wrapper(rendered)


if __name__ == '__main__':
    main()
