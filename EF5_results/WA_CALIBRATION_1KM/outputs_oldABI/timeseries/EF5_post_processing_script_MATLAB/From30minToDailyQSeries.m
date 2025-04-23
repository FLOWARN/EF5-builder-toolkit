sim_folder = '/vol_efthymios/NFS07/Data/aj1045/EF5WADomain/outputs/timeseries/timeseries_ghana/';

%For Ecuador, the daily observations of Q result from the average of measurements reported at 07h00 and 18h00 (Local Time GMT-0)

% Read in list of stations/gauges
stations_info = readtable('/vol_efthymios/NFS07/Data/aj1045/EF5WADomain/ghana_stations.csv')
% How many stations?
n_stations = numel(stations_info.Latitude);

% Create a datetime array of UTC times
delta_time = 1/(24*2); % Equates to 30-min intervals
sim_period = datetime('2001-01-01 00:00'):delta_time:datetime('2008-01-01 00:00');

study_period = datetime('2001-01-01'):datetime('2008-01-01');

% Use a buffer to account for errors in exact time of measurements
buffer30mins = 2;

% Create a datetime array of local times
local_sim_period = sim_period-0/24;

% Loop of list of gauges/stations
for st_i = 1:n_stations
	c_station = num2str(stations_info.StationCode(st_i));

    % Read in EF5 ts data
	sim_ts = readtable([sim_folder, 'ts.', c_station, '.crest.csv']);

	daily_ts = nan(size(study_period));

	cont_t = 0;

    % Time loop
    for t = study_period(2:end-1)
		cont_t = cont_t + 1;

				% Assumed times at which measurements are collected
				first_measurement = t+7/24; second_measurement = t+18/24;

        % Find time steps of measurements
        simQ_fm_ix = find(abs(local_sim_period - first_measurement) == min(abs(local_sim_period - first_measurement)));
		simQ_sm_ix = find(abs(local_sim_period - second_measurement) == min(abs(local_sim_period - second_measurement)));

        % Average values using a buffer
        if (simQ_fm_ix > 6)
			daily_ts(cont_t) = mean([sim_ts.Discharge_m_3S__1_(simQ_fm_ix-buffer30mins:simQ_fm_ix+buffer30mins); sim_ts.Discharge_m_3S__1_(simQ_sm_ix-buffer30mins:simQ_sm_ix+buffer30mins)]);
        else
			daily_ts(cont_t) = mean([sim_ts.Discharge_m_3S__1_(simQ_fm_ix); sim_ts.Discharge_m_3S__1_(simQ_sm_ix-buffer30mins:simQ_sm_ix+buffer30mins)]);
        end
    end

    % Write out a CSV
    outputTable = table(study_period', daily_ts', 'VariableNames', ["Date", "Daily Avg Q (cms)"]);
	writetable(outputTable, [sim_folder, 'daily_ts.', c_station, '.crest.csv'])
end
