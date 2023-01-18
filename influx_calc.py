#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Jan 18 13:50:51 2023

@author: szabi


CHCM -> Épp fűt-e/hűt-e a rendszer
CT -> Current temperature
RH -> Relative humidity
THCM -> Beállított fűtési mód
TT -> Target temperature
"""

from matplotlib import pyplot as plt

import pandas as pd

data_file=r"data/influxdata_2023-01-18T12_53_51Z.csv"

df_data=pd.read_csv(data_file,sep=',',error_bad_lines=False)


df_data=df_data.iloc[3:,5:]

df_data.columns=['Date','Value','Variable','HomeID','DevID','Zone']
df_data['Date2']=pd.to_datetime(df_data['Date'], infer_datetime_format=True)
df_data=df_data[df_data['Zone']=='Zone']
df_data=df_data[['Date2','Value','Variable','DevID']]
df_data=df_data.set_index('Date2')



devIDs=df_data['DevID'].unique()
variables=df_data['Variable'].unique()

df_data_grouped=df_data.groupby(['DevID','Variable'])
dev_keys=[key for key in  df_data_grouped.groups.keys() if key[0]=='1']

fig, axes = plt.subplots(nrows=len(variables), ncols=1, figsize=(12,4), sharey=True)

for (key, ax) in zip(dev_keys, axes.flatten()):
    ax.plot(df_data_grouped.get_group(key).index,df_data_grouped.get_group(key).Value)

ax.legend()
plt.show()