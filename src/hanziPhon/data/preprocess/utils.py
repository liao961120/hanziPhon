import re
import csv
import json
from dragonmapper.transcriptions import *

pat_hetero = re.compile(r'「(.+?)」的異體字')

tone_bpm = 'ˊˇˋ˙'
tone_py = '12345'

red = '（語音） （又音） （讀音） (又音) (讀音)'.split()
red2 = '（語音） （又音） （讀音） \(又音\) \(讀音\)'.split()
red2 = [ re.compile(f"{x}.*") for x in red2 ]

pinyin_custom = (
    # ori   corrected
    ('yúng', 'yóng'),
    ('lüǎn', 'lǖǎn'),
)


def get_word_phons(x:dict):
    phons = []
    for h in x.get('heteronyms', []):
        bpm = h.get('bopomofo', '').strip()
        pinyin = h.get('pinyin', '').strip()
        if len(bpm.split()) <= 1: continue

        # Clean up
        for pat in red2:
            bpm = pat.sub('', bpm).strip()
            pinyin = pat.sub('', pinyin).strip()
        
        bpm = tuple(bpm.split())
        pinyin = tuple(accented_syllable_to_numbered(x) for x in pinyin.split())

        phons.append({
            'bpm': bpm,
            'pinyin': pinyin,
        })
    
    return phons


def get_toned_bpm(d:dict):
    t = d['tone']
    tone = {
        '1': '',
        '2': 'ˊ',
        '3': 'ˇ',
        '4': 'ˋ',
        '5': '˙',
    }
    if t == '5':
        return '˙' + d['bpm']
    return d['bpm'] + tone[t]


def get_phons(x:dict):
    phons = []
    for h in x.get('heteronyms', []):
        try:
            bpm = h.get('bopomofo', '')
            pinyin = h.get('pinyin', '')
            if len(bpm.split()) != 1: continue

            for r in red:
                bpm = bpm.replace(r, "")
                pinyin = pinyin.replace(r, "")

            # Special cases
            for ori, cor in pinyin_custom:
                if ori == pinyin:
                    pinyin = cor

            # pinyin = zhuyin_to_pinyin(bpm, accented=True)
            pinyin = accented_to_numbered(pinyin)

            for t in tone_bpm:
                bpm = bpm.replace(t, '')

            for t in tone_py:
                if t in pinyin:
                    tone = t
                pinyin = pinyin.replace(t, '')
            if 'ㄦ' in bpm and len(bpm) >= 2: continue
            phons.append({
                'bpm': bpm,
                'pinyin': pinyin.strip(tone_py),
                'ipa': bpm_to_ipa(bpm), 
                'tone': tone,
            })
        except: 
            print(h)
            raise Exception('err')
            pass
            print(h)
            print()
    return phons


def get_ref_heteronyms(x:dict):
    title = x.get('title', '')
    if len(title) != 1: return
    for h in x.get('heteronyms', []):
        for d in h.get('definitions', []):
            d = d.get('def', '')
            m = pat_hetero.search(d)
            if m is not None:
                return m[1], title


bpm_ipa_map = {}
with open('transcriptions.csv', encoding="utf-8", newline='') as f:
    for row in csv.DictReader(f):
        bpm, ipa = row['Zhuyin'], row['IPA']
        bpm_ipa_map[bpm] = ipa


def bpm_to_ipa(bpm):
    return bpm_ipa_map[bpm]


def write_json(obj, fp):
    with open(fp, "w", encoding="utf-8") as f:
        json.dump(obj, f, ensure_ascii=False, separators=(',', ':'))


def load_json(fp):
    with open(fp, encoding='utf-8') as f:
        return json.load(f)
