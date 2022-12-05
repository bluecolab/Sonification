import pandas as pd
import apiCalls

def getStationDelta(station:str,days:int=2,hrs:int=None,mins:int=None):
    ''' For a given station, time delta, retrieve a data stream
        retrun as a dataframe for sonification
    '''
    data = apiCalls.getDataStreamDelta(station,days,hrs,mins)
    if isinstance(data, pd.DataFrame):
        return data
    else:
        return pd.DataFrame()
