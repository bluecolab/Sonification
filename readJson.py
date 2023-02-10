import json
import pandas as pd

def getJson(fileName = 'input.json') -> pd.DataFrame:
    jsonFile = pd.read_json(fileName)
    data = pd.json_normalize(jsonFile)
    return data

print(getJson())