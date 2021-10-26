import json
from pathlib import Path


class GuangYun:

    def __init__(self, lexicon:set=None) -> None:
        self._load()
        if lexicon:
            self.data = [ x for x in self.data if x['chr'] in lexicon ]
            
    
    def find(self, **kwargs):
        """Find hanzi from phonetic features
        """
        # yun_mu=None, sheng_mu=None, fan_qie=None, pinyin=None, ipa=None, tone=None
        return [
            x for x in self.data \
                if all( v in x[k] if isinstance(x[k], str) else (v in x[k])\
                        for k, v in kwargs.items())
        ]

    def match_all(self, data_x, kwargs):
        """Function to replace all() in self.find()
        """
        pass


    def query(self, char:str):
        """Query a hanzi for its phonetic representations
        """
        return [ x for x in self.data if char == x['chr'] ]


    def _load(self):
        data_dir = Path(__file__).parent / "data"
        with open(data_dir / "GuangYun.json", encoding="utf-8") as f:
            self.data = json.load(f)


#%%
