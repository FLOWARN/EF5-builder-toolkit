# Flash Flood Forecasting System for West Africa and Ghana

This repository contains code, documentation, data, and results from the research work done for NASA's SERVIR-West Africa project on developing a flash flood forecasting system in the West Africa domain (WA) (1km resolution) and Ghana domain (GH) (90m resolution).

This repository is split into 3 directories: DATA, EF5, CODES.

**1. Data**: Contains all data used in the research for both WA domain and GH domain, including a .xlsx file with observational station details is provided for both WA and GH domain.
**1.1. Subfolders for Ghana:**
    **GIS:** GIS files used to configure the study region, also flash flood event locations.
    **DATA_obs:** Observational streamflow data from different entities
    **Model_config:** Datasets needed to run Ghana high resolution model, such as basic grid files, parameters and forcings. This folder also contains instructions and inputs to calculate CREST and KW parameters.

**2. EF5_results:** Contains control files used for the WA and GH domain, as well as the simulation outputs. 

**3. Codes:** Contains python codes usefull for creating basic grid files, processing parameters layers, posprocessing EF5 outputs, download IMERG v07 files.

For any questions, contact Vanessa Robledo at vanessa-robledodelgado@uiowa.edu
