# downwards(1)

Wanna read wikipedia in a terminal using `man` ? No?

Here is your program anyways.

# usage

Installation

```
pip3 install .
```

and to use it

```
$ downwards --language de LOL > lol.1
$ man ./lol.1
```

and thats all. Enjoy

# background

I wanted to play around with OpenBSDs `mandoc` and learn how `mdoc` works.
Then I played around with Wikipedia and put both things togehter
