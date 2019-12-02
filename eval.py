#!/usr/bin/env python

import wikitextparser as wtp

text = '''

Emojis

== lachende Emojis ==

Alles was es hier zu wissen gibt überlachende emojies

== weinende Emojis ==

Mein gott das ist ja echt furchtbar

=== Verzweifelte Emojis ===

Aber es gibt auch richtig verzweiifelte emojis

== Verrückte Emojis ==

hier eine auswahl an anderen emojis
'''

sections = wtp.parse(text).sections

print("Plaintext")
print(text)
print('====================================')
print("Sections")
print(sections)
print('====================================')

for section in sections:
    print(".Sh " + section.title)
    sec = wtp.parse(section.contents).sections[0]
    print(sec.contents)


