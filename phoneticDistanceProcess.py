from g2p_en import G2p
import sys
import json

from g2p import make_g2p

text_to_send = list()


def to_phonetic(text_to_parse):
    out = transducer(text_to_parse)
    text_to_send.append(str(out))


transducer = make_g2p('eng', 'eng-arpabet')
text = "wild"
is_list = True
if is_list:
    list_from_string = text.strip('][').split(', ')
    for possibilitie in list_from_string:
        to_phonetic(possibilitie)
else:
    to_phonetic(text)
print(text_to_send)

