import re
import json
from pathlib import Path


class GuangYun:

    def __init__(self, lexicon:set=None) -> None:
        self._load()
        if lexicon:
            self.data = [ x for x in self.data if x['字'] in lexicon ]

    
    def find(self, return_raw=False, **kwargs):
        """Find hanzi from phonetic features
        """
        if return_raw:
            return [ x for x in self.data if match_all(x, kwargs) ]
        return { x['字'] for x in self.data if match_all(x, kwargs) }


    def query(self, char:str):
        """Query a hanzi for its phonetic representations
        """
        return self.find(return_raw=True, 字=char)
    

    @property
    def search_params(self):
        return list(self.data[0].keys())


    def _load(self):
        data_dir = Path(__file__).parent / "data"
        with open(data_dir / "GuangYun.json", encoding="utf-8") as f:
            self.data = json.load(f)



def match_all(data_x, kwargs):
    """A filter to compare data and search parameters
    """
    mn = 0
    for k, v in kwargs.items():
        if k not in data_x:
            print(f"[WARNING] condition {k} not in data")
            return False
        # ipa, pinyin, fan_qie
        v = re.compile(v)
        if isinstance(data_x[k], list):
            for item in data_x[k]:
                if v.search(item):
                    mn += 1
                    break
        else:
            if v.search(data_x[k]):
                mn += 1
    
    if mn == len(kwargs):
        return True
    return False

# %%
