import json
import pandas as pd
import urllib

# apiURL = 'http://localhost:8080/' # local - only when running api locally at this port
# apiURL = 'https://colabtest01.pace.edu/api/v1/' # test - only on pace vpn
# apiURL = 'https://colabprod01.pace.edu/api/v1/' # prod - this works everywhere
apiURL = 'http://api.bluecolab.cc/'

def getSensors() -> pd.DataFrame:
    # return all sensors
    call = 'v2/sensors/'
    try:
        sensors = pd.read_json(apiURL + call)
        return sensors
    except Exception as e:
        print(e)
        return pd.DataFrame()

def getDataStreamDelta(station:str,days:int,hrs:int=None,mins:int=None):
    # returns a stream of sensor data for a given station name and time delta
    # returns an error string if station doesn't exist
    queryString = 'stream=true&days={days}'
    qsargs = {'days': days}
    if hrs is not None:
        queryString += '&hours={hrs}'
        qsargs['hrs'] = hrs
    if mins is not None:
        queryString += '&minutes={mins}'
        qsargs['mins'] = mins
    args = {'station': station, 'queryString': queryString.format(**qsargs)}
    call = 'influx/sensordata/{station}/delta/?{queryString}'.format(**args)
    try:
        data = None
        with urllib.request.urlopen(apiURL + call) as src:
            jsonData = json.loads(src.read().decode())
            data = pd.json_normalize(jsonData)
        return data
    except Exception as e:
        print(e)
        print("error loading new data")
        return "can't load new data"