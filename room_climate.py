#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Mon Jan 23 08:57:40 2023

@author: szabi

<EID>: Entry ID
<AbsT>: Absolute timestamp [ms]
<RelT>: Relative timestamp [s]
<NID>: Node ID
Sensor Data:
<Temp>: Temperature [°C]
<RelH>: Relative Humidity [%]
<L1>: Light Sensor 1 (Wavelength) [nm]
<L2>: Light Sensor 2 (Wavelength) [nm]
Groundtruth:
<Occ>: Number of occupants (0, 1, 2)
<Act>: Activity of occupant(s) (0 = n/a, 1 = read, 2 = stand, 3 = walk, 4 = work)
<Door>: State of Door (0 = closed, 1 = open)
<Win>: State of Window (0 = closed, 1 = open)

"""

from matplotlib import pyplot as plt

import pandas as pd

data_file=r"/home/szabi/Projects/Room-Climate-Datasets/datasets-location_A/room_climate-location_A-measurement01.csv"

df_data=pd.read_csv(data_file,sep=',',error_bad_lines=False,header=None)

df_data.columns=['EID', 'AbsT', 'RelT', 'NID', 'Temp', 'RelH', 'L1', 'L2', 'Occ', 'Act', 'Door', 'Win']

df_data['Date2']=pd.to_datetime(df_data['AbsT'],unit="ms")

df_data_grouped=df_data.groupby(['NID'])


keys=list(df_data_grouped.groups.keys())

df_data_node=df_data_grouped.get_group(keys[0])

fig2, ax2 = plt.subplots()

ax2.plot(df_data_node['Date2'],df_data_node['Temp'])

plt.show()