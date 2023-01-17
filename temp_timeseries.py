# -*- coding: utf-8 -*-
"""
Created on Fri Jan 21 09:12:20 2022
@author: szabo
"""

#from io import BytesIO

#import requests

from matplotlib import pyplot as plt

import pandas as pd
sheet_id = '11WSTbHwSHVpiXz5OQ5GxFfDsV77dJ9pv_AtMTGeS3Jk'
sheet_gid = '1579323792'
sheet_url = f'https://docs.google.com/spreadsheets/d/{sheet_id}/edit#gid={sheet_gid}'

csv_export_url = sheet_url.replace('/edit#gid=', '/export?format=csv&gid=')


sp_code='1m'
conv_gas=10 # 1m3 gas heat power in kWh
price_gas=1
price_electric=1

### read google sheet
df_meter_data=pd.read_csv(csv_export_url,sep=',',error_bad_lines=False)
# cols=df_scale_data.columns

df_meter_data.columns=['Date','Gas','ElectricIn','ElectricOut','Solar','Water','Change','MeterageAtChange']
df_meter_data['Date2']=pd.to_datetime(df_meter_data['Date'], infer_datetime_format=True)

### spot METER replacement

ind_emeter_change=df_meter_data.loc[df_meter_data.loc[:,'Change']=='Elektromos mérőóra csere'].index
ind_gmeter_change=df_meter_data.loc[df_meter_data.loc[:,'Change']=='Gázmérő csere'].index

for i in ind_emeter_change:
    df_meter_data.loc[i+1:,'ElectricIn']+=df_meter_data.iloc[i].MeterageAtChange

for i in ind_gmeter_change:
    df_meter_data.loc[i+1:,'Gas']+=df_meter_data.iloc[i].MeterageAtChange

#### RESAMPLE

df_meter_resample_data=df_meter_data.copy()


df_meter_resample_data=df_meter_data[['Date2','Gas','ElectricIn','ElectricOut','Solar','Water']]
df_meter_resample_data=df_meter_resample_data.set_index('Date2')



df_meter_resample_data=df_meter_resample_data.resample(sp_code,origin='end').mean()
df_meter_resample_data=df_meter_resample_data.interpolate()

df_dmeter_resample_data=df_meter_resample_data-df_meter_resample_data.shift(1)


fig2, ax2 = plt.subplots()

ax2.plot(df_meter_resample_data.index,df_meter_resample_data['ElectricIn'],color='red',label='From GRID')
ax2.plot(df_meter_data['Date2'],df_meter_data['ElectricIn'],color='blue',label='From GRID')