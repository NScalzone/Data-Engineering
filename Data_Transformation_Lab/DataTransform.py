import pandas as pd
import numpy as np
from numpy import timedelta64
import statistics
import re

# csv_path = 'bc_trip259172515_230215.csv'
csv_path = 'larger_dataset.csv'

data = pd.read_csv(csv_path, usecols=['EVENT_NO_TRIP','OPD_DATE','VEHICLE_ID','METERS','ACT_TIME','GPS_LONGITUDE','GPS_LATITUDE'])

# data = pd.read_csv(csv_path)
# data.drop(columns='EVENT_NO_STOP')
# data.drop(columns='EVENT_NO_STOP')
# data.drop(columns='EVENT_NO_STOP')

# print(data)

dates = []


def filter_date(date_val):
    new_date = re.sub(":[0-9]{2}", "", date_val)
    return new_date    

def filter_act_time(act_time:str):
    next_day = 0
    time_val = float(act_time)
    seconds = time_val % 60
    minutes = (time_val - seconds) // 60
    hours = minutes // 60
    minutes = minutes - (hours * 60)
    check = seconds + (minutes * 60) + (hours * 60 * 60)
    if check != time_val:
        print('math mistake', check)
    hours = '{:02}'.format(int(hours))
    minutes =  '{:02}'.format(int(minutes))
    seconds =  '{:02}'.format(int(seconds))
    if int(hours) >= 24:
        # print("pre math hours is:", hours)
        hours = '{:02}'.format(int(hours) - 24)
        # print("hours is: ", hours)
        next_day = 1
    return[hours, minutes, seconds, next_day]

def get_timestamp(date_val, act_time):
    time = filter_act_time(act_time)
    
    #indicates that it's the next day
    if time[3]:
        day = int(date_val[:2])
        day += 1
        day = str(day)
        date_val = date_val[2:]
        date_val = day + date_val
    date_string = filter_date(date_val)+"T"+time[0]+time[1]+time[2]
    return pd.Timestamp(date_string)

# def get_timestamp_apply(framerow):
#     date_val = framerow['OPD_DATE']
#     act_time = framerow['ACT_TIME']
#     time = filter_act_time(act_time)
#     date_string = filter_date(date_val)+"T"+time[0]+time[1]+time[2]
#     return pd.Timestamp(date_string)

timestamps = []
for idx, row in data.iterrows():
    date_val = row['OPD_DATE']
    apt_time = row['ACT_TIME']
    timestamps.append(get_timestamp(date_val, apt_time))

data['TIMESTAMP'] = timestamps

data = data.drop(columns='OPD_DATE')
data = data.drop(columns='ACT_TIME')

speeds = [0.0]

diffs = data.diff()
# print(diffs)
for idx, row in diffs.iterrows():
    if pd.isnull(row['METERS']):
        pass
    else:
        time = row['TIMESTAMP']/timedelta64(1, 's')
        # print(time)
        speed = float(row['METERS']) / time
        speeds.append(speed)

data['SPEED'] = speeds



print(data)

print("max speed: ", max(speeds), "\nmin speed: ",min(speeds), "\nAverage speed: ", np.average(speeds))

print(data.loc[data['SPEED'] == 17.40])

print(data.median())


# verifying that the median of all data is also the median of just feb 15, which it turns out it is!
speeds_on_fifteenth = []
for idx, row in data.iterrows():
    if str(row['TIMESTAMP']).startswith('2023-02-15'):
        speeds_on_fifteenth.append(row['SPEED'])

print(statistics.median(speeds_on_fifteenth))
