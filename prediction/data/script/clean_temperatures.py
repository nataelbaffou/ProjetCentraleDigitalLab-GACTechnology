import pandas
import os
from pathlib import Path


path = [os.path.join(root,name).replace("\\",'/')
        for root,dirs,files in os.walk("C:/Users/CDL/Desktop/temperatures/")
        for name in files
        if name.endswith(".csv")]

for filepath in path : 
    data = pandas.read_csv(filepath, sep=';',parse_dates=['date'])
    data = data[['numer_sta','date','t']]
    data.to_csv(filepath,sep=';',index=False)