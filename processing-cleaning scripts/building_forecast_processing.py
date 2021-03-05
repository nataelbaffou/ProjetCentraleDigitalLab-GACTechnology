import pandas as pd

# Define paths
# TODO Change path to your initial files and storage directory
raw_path = "../data/raw/building_forecast/"
processed_path = "../data/processed/"

training_filename = "power-laws-forecasting-energy-consumption-training-data.csv"
test_filename = "power-laws-forecasting-energy-consumption-test-data.csv"
meta_filename = "power-laws-forecasting-energy-consumption-metadata.csv"
weather_filename = "power-laws-forecasting-energy-consumption-weather.csv"

# Charge files
training_df = pd.read_csv(raw_path + training_filename, sep=';', parse_dates=["Timestamp"])
test_df = pd.read_csv(raw_path + test_filename, sep=';', parse_dates=["Timestamp"])
meta_df = pd.read_csv(raw_path + meta_filename, sep=';')
weather_df = pd.read_csv(raw_path + weather_filename, sep=';', parse_dates=["Timestamp"])
print("Files charged")

dataset = pd.concat([training_df, test_df])
ids = meta_df["SiteId"].unique()

# For each building search for weathering data and create a file
for id_ in ids:
    temperatures = []
    data_spec = dataset[dataset["SiteId"] == id_].sort_values("Timestamp")
    weather_spec = weather_df[weather_df["SiteId"] == id_].sort_values("Timestamp")
    if not weather_spec.empty:
        for timestamp in data_spec["Timestamp"]:
            current_values = weather_spec[(weather_spec["Timestamp"] <= timestamp + pd.Timedelta(minutes=30))
                                          & (weather_spec["Timestamp"] >= timestamp - pd.Timedelta(minutes=30))]
            value = current_values["Temperature"].mean() if not current_values.empty else None
            temperatures.append(value)
    else:
        temperatures = [None] * data_spec.index.size
    data_spec["temperature"] = temperatures
    data_spec = data_spec.rename(columns={"Timestamp": "timestamp", "Value": "active_power"})
    data_to_store = data_spec[["timestamp", "active_power", "temperature"]]
    data_to_store = data_to_store.set_index(['timestamp'])
    data_to_store.to_csv(processed_path + str(id_) + ".csv", sep=';')


# Create and complete metadata file
days = ["monday", "tuesday", "wednesday", "thursday", "friday", "saturday", "sunday"]
Days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
with open(processed_path+"metadata.csv", "w") as f:
    f.write("bat_id;is_house;time_step;lat;long;surface;")
    f.write(";".join([e+"_is_off" for e in days]) + "\n")
    for id_ in ids:
        data_spec = dataset[dataset["SiteId"] == id_].sort_values("Timestamp")
        time_step = (data_spec["Timestamp"].iloc[1] - data_spec["Timestamp"].iloc[0]).total_seconds() / 60
        meta_spec = meta_df[meta_df["SiteId"] == id_]
        surface = meta_spec["Surface"].iloc[0]
        days_is_off = [meta_spec[Day+"IsDayOff"].iloc[0] for Day in Days]
        values = map(str, [id_, False, time_step, "", "", surface] + days_is_off)
        f.write(";".join(values) + "\n")

