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


sp_code='1d'
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

#### UPSAMPLE 

df_meter_resample_data=df_meter_data.copy()

df_meter_hf=df_meter_data[['Date2','Gas','ElectricIn','ElectricOut','Solar']]
df_meter_hf=df_meter_hf.set_index('Date2')

df_meter_hf=df_meter_hf.resample('6h',label='right',origin='end_day').ffill()
df_meter_hf=df_meter_hf.interpolate()

df_meter_hfdiff=df_meter_hf-df_meter_hf.shift(1)


# fig2, ax2 = plt.subplots()

# ax2.plot(df_meter_hf.index,df_meter_hf['ElectricIn'],color='red',label='From GRID')
# ax2.plot(df_meter_hf['Date2'],df_meter_hf['ElectricIn'],color='blue',label='From GRID')

# fig2, ax2 = plt.subplots()

# ax2.plot(df_meter_hfdiff.index,df_meter_hfdiff['ElectricIn'],color='red',label='From GRID')

##### RESAMPLE diffs
df_meter_diff=df_meter_hfdiff.resample(sp_code,label='right',origin='end_day').sum()

fig2, ax2 = plt.subplots()

ax2.plot(df_meter_diff.index,df_meter_diff['ElectricIn'],color='red',label='From GRID')