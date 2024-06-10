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

def read_and_convert(dataframe_gauge,file_obs,prefix):
    # Lee el archivo CSV
    data = dataframe_gauge
    
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
    
    ##Creo un Dataframe para guardar la precipitacion
    hourly_ppt = pd.DataFrame()
    # Convert half-hourly mm/h to actual precipitation
    hourly_ppt['Half-hourly Precip(mm)'] = data['Precip(mm h^-1)'] / 2
    
    total_precip_mm_day = hourly_ppt.groupby(pd.Grouper(freq='1D')).sum()
    
    Q_daily_df['Precip (mm d^-1)'] = total_precip_mm_day

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
    if not os.path.exists(path_data+"plots/"):
        os.makedirs(path_data+"plots/")
        
    fig, ax = plt.subplots(nrows=1, ncols=1,figsize=(30,10))
    ax1 = plt.subplot(1,1,1)
    ax1.scatter(Q_obs.index, Q_obs['discharge'], color = 'black', label='Observed')
    ax1.plot(Q_daily_df.index, Q_daily_df['Discharge(m^3 s^-1)'], color='blue', label='Simulated', linewidth=2)
    ax1.set_xlabel('Date', fontsize=20)
    ax1.set_ylabel('Discharge (m^3/s)',fontsize=20,color='blue')
    ax1.tick_params(axis='y', labelcolor='blue',labelsize=16)
    ax1.set_xlim(Q_daily_df.index.values[0], Q_daily_df.index.values[-1])
    ax1.xaxis.set_major_locator(AutoDateLocator(minticks=10, maxticks=20))
    ax1.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    ax1.tick_params(axis='x',labelsize=16,rotation=30)
    ax1.grid(True, which='major', linestyle='--', linewidth=0.5)
    
    # Create a secondary y-axis
    ax2 = ax1.twinx()
    ax2.plot(Q_daily_df.index,Q_daily_df['Precip (mm d^-1)'],color='rebeccapurple',linewidth=2, alpha = 0.7)
    ax2.set_ylim(0,Q_daily_df['Precip (mm d^-1)'].max()+50)
    ax2.invert_yaxis()
    ax2.set_ylabel('Precip (mm d^-1)', color='rebeccapurple',fontsize=20)  # we already handled the x-label with ax1
    ax2.tick_params(axis='y', labelcolor='rebeccapurple',labelsize=16)
    ax2.yaxis.set_major_locator(MaxNLocator(nbins=10))
    
    # Trazar las dos series de tiempo
    #plt.plot(Q_daily_df.index, Q_daily_df['Max'], color = 'grey',linewidth=3)
    #plt.plot(Q_daily_df.index, Q_daily_df['Min'], color = 'grey',linewidth=3)
    # Agregar una sombra entre las dos líneas
    #plt.fill_between(Q_daily_df.index, Q_daily_df['Max'], Q_daily_df['Min'], color='grey', alpha=0.3)
    #plt.plot(observations.index, observations['discharge'], label=file[len(prefix)+3:-10])
    
    # Agrega texto con métricas
    ax = plt.gca()
    plt.text(0.02, 0.95, f'RMSE: {rmse:.2f}\nBias: {bias:.2f}\nNSE: {nse:.2f}', transform=ax.transAxes, fontsize=16,
             verticalalignment='top', bbox=dict(boxstyle='round', facecolor='white', alpha=0.9))
    plt.legend()
    
    #plt.xticks(rotation=30, fontsize=16)

    plt.title('GAUGE= '+file[len(prefix)+3:-10])
    plt.grid(visible=True, which='major')
    ax.xaxis.set_major_locator(AutoDateLocator(minticks=10, maxticks=20))
    ax.xaxis.set_major_formatter(DateFormatter('%Y-%m-%d'))
    #plt.show()
    plt.savefig(path_data+"plots/"+file[len(prefix)+3:-10]+'.png',bbox_inches='tight')
#%%   
path_data= '/Users/vrobledodelgado/Library/CloudStorage/OneDrive-UniversityofIowa/PhD/SERVIR_PROJECT/GHANA/Calibration/OUTPUTS_90m/baseline3/'
path_obs = '/Users/vrobledodelgado/Documents/GitHub/FFWestAfrica/DATA/GHANA/DATA/consolidated/'

file_list_obs = glob.glob(path_obs + "*.csv")
print((file_list_obs))
prefix_obs = path_obs

#%%
for file_obs in file_list_obs:
    # Extract the number from the current file
    #num_file = file_obs[len(prefix_obs):-len('_daily_Q.csv')].strip()
    #%%
    file_obs = file_list_obs[0]
    num_file = '9000008'
    gauge = []
    print('looking for files in gauge: ',num_file)
    for y in range(2002,2023):
        year = str(y)
        path_data2 = path_data+year+'/'
        file_list = glob.glob(path_data2 + "*.csv")
        print('Files in', path_data2, ':', file_list)
        prefix = path_data2
        
        for file in file_list:
            num_file_obs = file[len(prefix)+3:-len('.crest.csv')].strip()
            print('Comparing num_file:', num_file)
            print('With num_file_obs:', num_file_obs)
            matching_file_obs = None
            
            if num_file_obs == num_file:
                print('there is matching file:',num_file, num_file_obs)
                #abro el archivo y le quito los primeros meses (el warmup)
                ef5_file = pd.read_csv(file, sep =',')
                ef5_file['Time'] =  pd.to_datetime(ef5_file['Time'])
                gauge.append(ef5_file)
                print(len(gauge))
                print('file: ', num_file, ' from year: ', year, ' was append')
                matching_file_obs = file_obs
                break
            
    if matching_file_obs:
        combined_df = pd.concat(gauge, ignore_index=True)
        combined_df.set_index('Time', inplace=True)
        #creating calcutlations and plots
        Q_daily_df, Q_obs = read_and_convert(combined_df, file_obs, prefix)
        initial_data = Q_obs.index[0]
        final_data = Q_obs.index[-1]
        Q_daily_df_2 = Q_daily_df.loc[(Q_daily_df.index >= initial_data) & (Q_daily_df.index <= final_data)]
        rmse, bias, nse = calcular_metricas_error(Q_daily_df_2['Discharge(m^3 s^-1)'], Q_obs['discharge'])
        #%%
        plotting(Q_daily_df_2, Q_obs, nse, bias, rmse)



# %%
