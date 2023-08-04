% This script produces PNG files from the IMERG data. Then, to create animations run 'convert -loop 0 -delay 10 {file_input_names} {output_name}' in the command line 

clc; clear; % Start with "a clean slate"

% Time period of interest
imerg_period = datetime('18-Jun-2018 21:00'):1/(24*2):datetime('19-Jun-2018 21:00');

% Path to your precip (inout folder)
precip_folder = '/vol_efthymios/NFS07/Data/aj1045/imerg/early_run/';

% Path to your resulting PNGs images (output folder)
pngs_folder = '/vol_efthymios/NFS07/Data/aj1045/imerg/animations/png_files/';

% WA domain
wa_boundaries = shaperead("/vol_efthymios/NFS07/Data/aj1045/EF5WADomain/gis/SERVIR_plus_USAID_Countries/wa_countries_combined.shp", "UseGeoCoords", true);

% Load precip color ramp
load("/vol_efthymios/NFS07/Data/aj1045/imerg/animations/Precipitation_Colormap.mat");

% Time loop
% Read first file to set variables
t = imerg_period(1);
% Get geographical information
mapinfo = geotiffinfo([precip_folder, 'imerg.', char(t, 'yyyyMMddHHmm'), '.30minAccum.tif']);
RefMatrix = mapinfo.RefMatrix;

% Read in precip file
c_precip = imread([precip_folder, 'imerg.', char(t, 'yyyyMMddHHmm'), '.30minAccum.tif']);

% Make zero anything below zero
c_precip(c_precip<0) = 0;

%% Plotting

% PNG's resolution
resolution = 0; % If 0, uses system's default resolution. Value should be an integer value indicating the resolution in dots per inch

% Precip domain
xmin = -21.4; xmax = 30.4; ymin = -2.9; ymax = 33.1;
rep_x = -4.018;  %add longitude coordinates of event
rep_y = 5.321;  %add latitude coordinates of event
% Instantaneous data
figure(1);
% Plot precip field
h_precip = geoshow(double(c_precip.*2), RefMatrix, 'DisplayType','texturemap'); clim([0 25]);
% Plot boundaries
geoshow(wa_boundaries,"FaceColor","none", "EdgeColor","k");
% Add report coordinates
hold all;
scatter(rep_x, rep_y, 100, 'k', 'filled');
% Axes settings
set(gca, 'Xlim', [xmin-0.05 xmax+0.05], 'Ylim', [ymin-0.05 ymax+0.05], 'FontSize', 14); box on;
% Color ramp settings
colormap(precip_cmap); hbar = colorbar(); ylabel(hbar, 'Precipitation Rates (mm/hr)', 'FontSize', 16);
% Title of plot
h_title = title(char(t, 'yyyyMMdd HH:mm'), 'FontSize', 14);

% Cumulative data
figure(2);
% Plot precip field
h_cumprecip = geoshow(double(c_precip), RefMatrix, 'DisplayType','texturemap'); clim([0 250]);
% Plot boundaries
geoshow(wa_boundaries,"FaceColor","none", "EdgeColor","k");
% Add report coordinates
hold all;
scatter(rep_x,rep_y, 100, 'k', 'filled');
% Axes settings
set(gca, 'Xlim', [xmin-0.05 xmax+0.05], 'Ylim', [ymin-0.05 ymax+0.05], 'FontSize', 14); box on;
% Color ramp settings
colormap(precip_cmap); hbar = colorbar(); ylabel(hbar, 'Cumulative Precipitation (mm)', 'FontSize', 16);
% Title of plot
h_cumtitle = title(char(t, 'yyyyMMdd HH:mm'), 'FontSize', 14);

% Create an accumulation variable
accum_precip = zeros(size(c_precip));

pause(0.5);

resStr = num2str(int16(resolution));
for t = imerg_period(2:end)
    c_precip = imread([precip_folder, 'imerg.', char(t, 'yyyyMMddHHmm'), '.30minAccum.tif']);
    % Make zero anything below zero
    c_precip(c_precip<0) = 0;

    % Accumulate precip
    accum_precip = accum_precip + c_precip;

    % Update figure 1
    h_precip.CData = double(c_precip.*2);
    h_title.String = char(t, 'yyyyMMdd HH:mm');
    print(figure(1), [pngs_folder, 'precip.', char(t, 'yyyyMMddHHmm'), '.png'], ['-r', resStr], '-dpng');

    % Update figure 2
    h_cumprecip.CData = double(accum_precip);
    h_cumtitle.String = char(t, 'yyyyMMdd HH:mm');
    % Save
    print(figure(2),[pngs_folder, 'cumprecip.', char(t, 'yyyyMMddHHmm'), '.png'], ['-r', resStr], '-dpng');

    pause(0.5);
end

close all; %Close all figure windows

% exit; % Close program in server
