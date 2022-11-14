import pandas as pd
import urllib.request
from sonify import sonify
import numpy as np
from .influxModels import getStationDelta
from .apiCalls import getSensors
import pandas as pd

# define the columns to pull for different types of data
# Temp, pH, Cond, DOpct, Turb, Sal
WATER_VALUES = [1,2,4,5,8,10] 
# AirTemp, Rain, MaxWindSpeed, VaporPressure, BaroPressure
WEATHER_VALUES = [18,12,17,19,20]

# define sounds for different types of data
# Temp, pH, Cond, DOpct, Turb, Sal
WEATHER_SOUNDS = ['orchestral harp','choir aahs','church organ','violin','cello']

# AirTemp, Rain, MaxWindSpeed, VaporPressure, BaroPressure
WATER_SOUNDS = ['orchestral harp','choir aahs','church organ','viola','violin','cello']


def SaveFile(station:str = 'Ada'):
    
    #reading the data
    data = None

    try:
        data = getStationDelta(station, 2)
        data.replace(0.,np.nan, inplace=True)

        # set local params
        if station == "Odin": 
            # odin - weather
            cols = WEATHER_VALUES
            sounds = WEATHER_SOUNDS
        else:
            # ada - choate pond
            cols = WATER_VALUES
            sounds = WATER_SOUNDS

        # pull sensors
        sensors = getSensors()

        input_data = []
        for i, col in enumerate(cols):
            # pull column from dataframe
            col_name = 'sensors.' + sensors.loc[sensors['SensorID'] == col, 'SensorName'].item()

            col_data = data[col_name]
            input_data.append([sounds[i]] + list(zip(range(0, len(col_data)), col_data)))
        
        # play!
        sonify.play_midi_from_data(input_data, track_type='multiple', key = 'd_sharp_major', file_name='dashboard/static/data/' + station.lower() + '.mid')
        return(True)
    except (urllib.error.URLError, KeyError) as e:
        return "We're sorry, can't load new data right now. Please enjoy this sonification of some of our previous data."
    except TypeError as e:
        return "Sorry, we can't find any data for that station."