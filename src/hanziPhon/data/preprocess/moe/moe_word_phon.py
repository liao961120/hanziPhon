#%%
import json
from collections import Counter
from utils import get_word_phons, write_json

with open('moe.json', encoding='utf-8') as f:
    moe = json.load(f)

with open('moe_char_phon.json', encoding='utf-8') as f:
    moe_chr = json.load(f)
    moe_chr = set(moe_chr.keys())


# %%
word_phons = {}
for d in moe:
    t = d['title']
    if t in moe_chr: continue

    phons = get_word_phons(d)
    if len(phons) > 0:
        word_phons[t] = phons

write_json(word_phons, 'moe_word_phon.json')

