# Flash Flood Forecasting System for West Africa: EF5 directory 

The EF5 directory contains control files used for the West Africa domain, as well as the simulation outputs of max unit streamflow and discharge timeseries.


There are control files to produce timeseries outputs, and map outputs of max unit streamflow and precipitation accumulation. There is also a timeseries control file for only Ghana gauge stations. A word doc is also included, for info on the gauge stations and their locations. 

The outputs subdirectory is split into maps, timeseries, and ghana_skill_assessment. Maps contains map outputs for 5 flash flood events. Timeseries contains a MATLAB script to post-process the simulated timeseries outputs, so that they can be compared to observational data. EF5's timeseries output files, run for all gauge stations in the West Africa domain, were too big to add to this repository, but can be found in the Rutgers system at '/vol_efthymios/NFS07/Data/aj1045/EF5_outputs'. Ghana_skill_assessment contains timeseries data specifically for Ghana gauge stations (here EF5 outputs have been post-processed and are re-named to 'daily_ts.1531600.crest.csv' for gauge station 1531600, for example), as well as hydrograph plots produced comparing EF5 simulations with observational data for these gauge stations. This outputs subdirectory also contains a jupyter notebooks script to produce hydrograph plots comparing EF5 timseries outputs to observational data. 
