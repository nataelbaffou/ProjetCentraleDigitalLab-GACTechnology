from pathlib import Path 
import os
import pandas as pd 

os.chdir(r"C:\Users\CDL\Desktop\prediction\data")
liste = os.listdir(r"C:\Users\CDL\Desktop\prediction\data")
init = False
col = ["bat_id","is_house","time_step","lat","long","surface","monday_is_off","tuesday_is_off","wednesday_is_off","thursday_is_off","friday_is_off","saturday_is_off","sunday_is_off"]
metadata = pd.DataFrame(columns=col)
for filename in liste:
    if filename.find(".csv") != -1:
        data = pd.read_csv(filename,sep=";")
        metadata = metadata.append(data)

metadata = metadata.sort_values(by=['bat_id'])
metadata.to_csv('metadataCompleted.csv',sep=';',index=False)
print('done')