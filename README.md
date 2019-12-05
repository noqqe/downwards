# downwards

You want to read a wikipedia page right from your terminal, right? RIGHT?

I know because I wanted it.

`downwards` is downloading the article you want, converts it to `mdoc` and
displays it using your local `man` binary.

```
$ downwards OpenBSD
$ downwards 'Theo de Raadt'
$ downwards 'Python (Programming Langauge)'
$ downwards --help
Usage: downwards [OPTIONS] ARTICLE

  downwards lets you read a wikipedia page on command line as a manpage.

Options:
  -l, --language TEXT  Language for wikipedia
  -s, --stdout         Print to stdout
  --help               Show this message and exit.
```

I found it very helpful to set `export MANWIDTH=80` for nicely readable
documents.

![Image of an Example Wikipedia Page](https://raw.githubusercontent.com/noqqe/downwards/master/screenshot.png)

# Installation

Installation

```
pip3 install downwards
```

Development

```
pip3 install --upgrade .
```

# Background

I wanted to play around with OpenBSDs `mandoc` and learn how `mdoc` works.
Then I played around with Wikipedia and put both things together.

However, once I got a first prototype up and running, I started liking it. It
feels like a "reader"-feature from your browser, but only from your terminal
right at hand.

# Bugs and Known Issues

There are always some things in automatically generated mdoc documents that
throw warnings. Since you cannot make `man` ignoring them, I need to press
`ctrl+l` to reset those warnings.

`man` is really not made to display a wide range of special utf8 characters
(neither on OpenBSD, Linux nor macOS). I've done what I can to strip those
away or replace german umlauts with `ae` for example.

