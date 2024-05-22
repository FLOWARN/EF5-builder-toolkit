#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
This code convert 30 min Q to daily Q

@author: vrobledodelgado
"""
#%%
import pandas as pd
import numpy as np
import glob
import matplotlib.pyplot as plt
from datetime import timedelta
import glob
import time
from matplotlib.dates import DateFormatter, AutoDateLocator
import os

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
    if not os.path.exists(path_data+"dailyQ/"):
        os.makedirs(path_data+"dailyQ/")
        
    Q_daily_df.to_csv(path_data+"dailyQ/"+file[len(prefix):])
    print('Saving :'+ file[len(prefix):])
    
    Q_observed = pd.read_csv(file_obs, parse_dates=['date'], index_col='date')
    Q_observed_filtered = Q_observed[Q_observed.index.year >= 2000]
    
    return Q_daily_df,Q_observed_filtered

def calcular_metricas_error(df_simulado, df_observado):
    # Unir los DataFrames en función de las fechas que coincidan
    df_merged = pd.merge(df_simulado, df_observado, how='outer', left_index=True, right_index=True, suffixes=('_simulado', '_observado'))
    
    # Calcular métricas de error solo para las filas donde haya valores en ambos DataFrames
    df_valid = df_merged.dropna(subset=['Discharge(m^3 s^-1)', 'discharge'])
    from sklearn.metrics import mean_squared_error
    rmse = mean_squared_error(df_valid['discharge'],df_valid['Discharge(m^3 s^-1)'],squared=False)
    bias = (df_valid['Discharge(m^3 s^-1)'] - df_valid['discharge']).mean()
    nse = 1 - ((df_valid['Discharge(m^3 s^-1)'] - df_valid['discharge']) ** 2).sum() / ((df_valid['discharge'] - df_valid['discharge'].mean()) ** 2).sum()
    
    return rmse, bias, nse

def plotting(Q_daily_df, Q_obs, nse, bias, rmse):
    fig = plt.subplots(figsize=(16, 5))
    plt.scatter(Q_obs.index, Q_obs['discharge'], color = 'black', label='Observed')
    plt.plot(Q_daily_df.index, Q_daily_df['Discharge(m^3 s^-1)'], color = 'blue', label='Simulated', linewidth=4)
    
    # Trazar las dos series de tiempo
    #plt.plot(Q_daily_df.index, Q_daily_df['Max'], color = 'grey',linewidth=3)
    #plt.plot(Q_daily_df.index, Q_daily_df['Min'], color = 'grey',linewidth=3)
    # Agregar una sombra entre las dos líneas
    #plt.fill_between(Q_daily_df.index, Q_daily_df['Max'], Q_daily_df['Min'], color='grey', alpha=0.3)
    #plt.plot(observations.index, observations['discharge'], label=file[len(prefix)+3:-10])
    # Agrega texto con métricas
    ax = plt.gca()
    plt.text(0.02, 0.95, f'RMSE: {rmse:.2f}\nBias: {bias:.2f}\nNSE: {nse:.2f}', transform=ax.transAxes, fontsize=12,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.5))

    plt.legend()
    plt.xlabel('Date', fontsize=18)
    plt.ylabel('Discharge (m^3/s)',fontsize=18)
    plt.xticks(rotation=30, fontsize=15)
    plt.yticks(fontsize=15)
    plt.xlim(Q_daily_df.index.values[0], Q_daily_df.index.values[-1])
    #plt.ylim(0,Q_daily_df['Discharge(m^3 s^-1)'].max()+15)
    plt.title('GAUGE= '+file[len(prefix)+3:-10])
    plt.grid(visible=True, which='major')
    ax.xaxis.set_major_locator(AutoDateLocator(minticks=10, maxticks=20))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m'))
    #plt.show()
    plt.savefig(path_plots+file[len(prefix)+3:-10]+'.png',bbox_inches='tight')

#%%
#read all the files
path_data= '/Users/vrobledodelgado/Library/CloudStorage/OneDrive-UniversityofIowa/PhD/SERVIR_PROJECT/GHANA/Calibration/OUTPUTS_90m/baseline2/outputs/'
path_plots = '/Users/vrobledodelgado/Library/CloudStorage/OneDrive-UniversityofIowa/PhD/SERVIR_PROJECT/GHANA/Calibration/OUTPUTS_90m/baseline2/plots/'
path_obs = '/Users/vrobledodelgado/Documents/GitHub/FFWestAfrica/DATA/GHANA/DATA/consolidated/'

file_list = glob.glob(path_data + "*.csv")
print((file_list))
prefix = path_data

file_list_obs = glob.glob(path_obs + "*.csv")
print((file_list_obs))
prefix_obs = path_obs

for file, file_obs in zip(file_list,file_list_obs):
    print('Opening: ' + file[len(prefix):])
    Q_daily_df, Q_obs = read_and_convert(file, file_obs, prefix)
    rmse, bias, nse = calcplotsular_metricas_error(Q_daily_df['Discharge(m^3 s^-1)'], Q_obs['discharge'])
    plotting(Q_daily_df,Q_obs,nse,bias,rmse)
# %%
