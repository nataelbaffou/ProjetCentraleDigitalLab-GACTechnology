import pandas as pd
import os
import numpy as np

station_list = pd.read_csv("/Users/pasqua/Downloads/postesSynop.csv",sep=";")

data = pd.read_csv("/Users/pasqua/Downloads/household_power_consumption.csv",sep=";",parse_dates=[[0,1]],na_values="?")
data = data.set_index('Date_Time')
data = data.dropna(how='all')

data_cleaned = pd.DataFrame({'timestamp':data.index.values,
    'active_power':data['Global_active_power'].values})

sceaux_lat = 48.778
sceaux_long = 2.2951

surface = None
time_step = 1
id = 4000

meta_file_name = "metadata.csv"
file_name = "{}.csv".format(id)

dist = np.array([(station_list["Latitude"].values[i]-sceaux_lat)**2
    +(station_list["Longitude"].values[i]-sceaux_long)**2
     for i in range(station_list["Longitude"].values.shape[0])])

id_station = station_list["ID"][np.argmin(dist)]

print(id_station)



