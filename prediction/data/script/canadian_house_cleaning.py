import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# TODO change paths if necessary
raw_path = "../data/raw/almanac/"
processed_path = "../data/processed/almanac/"
power_filename = "Electricity_P.csv"
weather_filename = "Climate_HourlyWeather.csv"

building_id = 3000

power_df = pd.read_csv(raw_path + power_filename, sep=',', parse_dates=["UNIX_TS"],
                       date_parser=lambda col: pd.to_datetime(col, unit='s'))
weather_df = pd.read_csv(raw_path + weather_filename, sep=',', parse_dates=["Date/Time"])

power_df.rename(columns={"UNIX_TS": 'timestamp', "MHE": "active_power"}, inplace=True)
weather_df.rename(columns={"Date/Time": 'timestamp', "Temp (C)": 'temperature'}, inplace=True)

merged_df = power_df[["timestamp", "active_power"]].merge(weather_df[['timestamp', 'temperature']])
merged_df.interpolate(inplace=True)

merged_df.to_csv(processed_path + str(building_id) + ".csv", sep=';', index=False)
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
with open(processed_path + "metadata.csv", "w") as f:
    f.write("bat_id;is_house;time_step;lat;long;surface;")
    f.write(";".join([e + "_is_off" for e in days]) + "\n")
    values = map(str, [building_id, True, 1, "49.247139", "-122.950778", 199, "", "", "", "", "", "", ""])
    f.write(";".join(values) + "\n")
