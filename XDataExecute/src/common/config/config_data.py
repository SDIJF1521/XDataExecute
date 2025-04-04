# XDataExecute/config/config_data.py

import json
import pandas as pd


class GaiJson:
    def gain(self,config_json=None):
        if config_json is None:
            config_json = './data_config.json'
        with open(config_json, 'r', encoding='utf-8') as file:
            data = json.load(file)
        return pd.Series(data)
