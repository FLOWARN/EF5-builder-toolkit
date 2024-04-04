#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code convert 30 min Q to daily Q

@author: vrobledodelgado
"""
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from datetime import timedelta
import glob
import time
from matplotlib.dates import DateFormatter, AutoDateLocator

def read_and_convert(file,file_obs,prefix):
    # Lee el archivo CSV
    data = pd.read_csv(file, parse_dates=['Time'], index_col='Time')
    
    # Filtra las mediciones de las 7 am y 6 pm
    data_7am = data.between_time('07:00:00', '07:10:00')
    data_6pm = data.between_time('18:00:00', '18:10:00')
    
    dump_df = pd.concat([data_7am['Discharge(m^3 s^-1)'],data_6pm['Discharge(m^3 s^-1)']])
    means = dump_df.groupby(pd.Grouper(freq='1D')).mean()
    maximum = data.groupby(pd.Grouper(freq='1D')).max()
    minimum = data.groupby(pd.Grouper(freq='1D')).min()
    
    # Agrupa por día y calcula el máximo y mínimo diario
    Q_daily_df = pd.DataFrame(index=means.index)
    Q_daily_df['Discharge(m^3 s^-1)'] = means
    Q_daily_df['Max'] = maximum['Discharge(m^3 s^-1)']
    Q_daily_df['Min'] = minimum['Discharge(m^3 s^-1)']
    
    #Saving my new Q daily files
    Q_daily_df.to_csv(path_data+"dailyQ/"+file[len(prefix):])
    print('Saving :'+ file[len(prefix):])
    
    Q_observed = pd.read_csv(file_obs, parse_dates=['date'], index_col='date')
    
    return Q_daily_df,Q_observed


def plotting(Q_daily_df, Q_obs):
    fig = plt.subplots(figsize=(16, 5))
    plt.plot(Q_daily_df.index, Q_daily_df['Discharge(m^3 s^-1)'], color = 'blue', label='Simulated', linewidth=4)
    plt.scatter(Q_obs.index, Q_obs['discharge'], color = 'black', label='Observed')

    # Trazar las dos series de tiempo
    plt.plot(Q_daily_df.index, Q_daily_df['Max'], color = 'grey',linewidth=3)
    plt.plot(Q_daily_df.index, Q_daily_df['Min'], color = 'grey',linewidth=3)
    # Agregar una sombra entre las dos líneas
    plt.fill_between(Q_daily_df.index, Q_daily_df['Max'], Q_daily_df['Min'], color='grey', alpha=0.3)
    #plt.plot(observations.index, observations['discharge'], label=file[len(prefix)+3:-10])
    plt.legend()
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Discharge (m^3/s)',fontsize=18)
    plt.xticks(rotation=30, fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim(Q_daily_df.index.values[0], Q_daily_df.index.values[-1])
    #plt.ylim(0,Q_daily_df['Discharge(m^3 s^-1)'].max()+15)
    plt.title('GAUGE= '+file[len(prefix)+3:-10])
    plt.grid(visible=True, which='major')
    ax = plt.gca()
    ax.xaxis.set_major_locator(AutoDateLocator(minticks=10, maxticks=20))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    #plt.show()
    plt.savefig(path_plots+file[len(prefix)+3:-10]+'.png',bbox_inches='tight')



#read all the files
path_data= '/Users/vrobledodelgado/Library/CloudStorage/OneDrive-UniversityofIowa/PhD/SERVIR_PROJECT/GHANA/Calibration/outputs/'
path_plots = '/Users/vrobledodelgado/Library/CloudStorage/OneDrive-UniversityofIowa/PhD/SERVIR_PROJECT/GHANA/Calibration/outputs/plots/'
path_obs = '/Users/vrobledodelgado/Library/CloudStorage/OneDrive-UniversityofIowa/PhD/SERVIR_PROJECT/GHANA/Calibration/GaugeStations/gauges/fixeddata/'

file_list = glob.glob(path_data + "*.csv")
print((file_list))
prefix = path_data

file_list_obs = glob.glob(path_obs + "*.txt")
print((file_list_obs))
prefix_obs = path_obs



for file, file_obs in zip(file_list,file_list_obs):
    print('Opening: ' + file[len(prefix):])
    Q_daily_df, Q_obs = read_and_convert(file, file_obs, prefix)
    plotting(Q_daily_df,Q_obs)
    
    


