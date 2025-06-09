# Building an EF5 Model: A Step-by-Step Guide

A complete guide to constructing and implementing an EF5 model from scratch using Python and Jupyter Notebooks.

## Overview
This repository provides a step-by-step guide for setting up an EF5 model configuration. The included code and resources are designed to help users build a functional model for their own watershed. The methodology outlined here has been successfully used to create EF5 models at various resolutions for regions like Ghana, West Africa, and Iowa, USA.

The core of the EF5 model is the **control file**, which defines all the input data and parameters. This guide is structured around filling out the necessary blocks within this control file.

For a comprehensive understanding of EF5, please refer to the official documentation: [EF5 User Manual](https://ef5docs.readthedocs.io/).

For any questions, contact Vanessa Robledo (vanessa-robledodelgado@uiowa.edu).

---

## Prerequisites

You have two options for running the code in this guide:

#### 1. Google Colaboratory (Recommended)
The easiest way to get started is with Google Colab, as all notebooks are adapted to run in that environment.
- **Link:** [https://colab.research.google.com/](https://colab.research.google.com/)

#### 2. Local Conda Environment
If you prefer to work on your local machine, we recommend creating a new Conda environment to avoid package conflicts.

1.  **Create the environment from the provided file:**
    The `environment.yml` file is located in the `/prerequisites` folder. Run the following command in your terminal:
    ```sh
    conda env create -f prerequisites/environment.yml
    ```
    *(This process may take several minutes.)*

2.  **Activate the new environment:**
    ```sh
    conda activate ef5_env
    ```

---

## 📁 Project Structure

All necessary files are organized into the following folders:

-   **/Codes:** Contains all Jupyter Notebooks for each step.
-   **/prerequisites:** Includes the Conda environment file.

---

## Step-by-Step Instructions

The following steps will walk you through generating the required input files for the EF5 model, using the control file blocks as our guide.


### Step 1: Getting the basic files

This first step creates the fundamental raster files: the Digital Elevation Model (DEM), Flow Direction Model (DDM), and Flow Accumulation Model (FAM).

**EF5 Control File Block:**
```
[Basic]
DEM=data/basic/dem.tif
DDM=data/basic/ddm.tif
FAM=data/basic/fam.tif
PROJ=geographic
ESRIDDM=true
SelfFAM=false
```
First step is to get the basic grid files (DEM, flow direction, flow accumulation). Users have several options such as QGIS or ArcGIS based methodologies. However, in this tutoral you have two options depending on your available data:

* **Option A: Use HydroSHEDS Data**
    If you want to create a model based on the readily available HydroSHEDS dataset, use the following notebook:
    - **Notebook:** [`/Codes/1_GettingBasicFiles.ipynb`](/Codes/1_GettingBasicFiles.ipynb)

* **Option B: Use a Custom DEM**
    If you have your own high-resolution DEM, use this notebook to derive the DDM and FAM grids:
    - **Notebook:** [`/Codes/1b_CreateBasicGrids.ipynb`](/Codes/1b_CreateBasicGrids.ipynb)


**Result:** After running the appropriate notebook, ensure your three output files (`dem.tif`, `ddm.tif`, `fam.tif`) are saved in the `/data/basic/` directory.

### Step 2: Prepare Precipitation Forcing Data

Next, you will download and format the precipitation data. This guide uses IMERG v07 for its excellent spatial and temporal resolution.

**EF5 Control File Block:**
```
[PrecipForcing IMERG]
TYPE=TIF
UNIT=mm/h
FREQ=30u
LOC=/data/precip/
NAME=imerg.YYYYMMDDHHUU.tif
```
In this example, we are using IMERG v07 files due to its high temporal and spatial coverage. Follow the instructions in the notebook below to process the precipitation files.
- **Notebook:** [`/Codes/2_Get_precipitation_files.ipynb`](/Codes/2_Get_precipitation_files.ipynb)

**Result:** Place all generated precipitation `.tif` files into the `/data/precip/` directory.

### Step 3: Prepare Potential Evapotranspiration (PET) Data

The final forcing dataset required is Potential Evapotranspiration.

**EF5 Control File Block:**
```
[PETForcing CLIMO]
TYPE=TIF
UNIT=mm/d
FREQ=1m
LOC=/data/pet/
NAME=PET.MM.tif
```

You can obtain PET data from several sources:

* **Global Dataset:** The University of Oklahoma provides global PET datasets compatible with EF5. You can find them in the [EF5-Global-Parameters](https://github.com/HyDROSLab/EF5-Global-Parameters/tree/main/FAO_PET) repository.
* **Regional Dataset (West Africa):** If you are building the West Africa or Ghana 1km model, pre-clipped PET files are available [here](https://github.com/RobledoVD/WAEF5-dockerized/tree/main/data/pet).

**Result:** Place the monthly PET `.tif` files (e.g., `PET.01.tif`, `PET.02.tif`, etc.) into the `/data/pet/` directory.

### Step 4: In process....







```
[Task BASINAVGING] 
STYLE=BASIN_AVG 
MODEL=crest 
ROUTING=KW 
BASIN=0 
PRECIP=IMERG 
PET=CLIM 
OUTPUT=/basin-aggregation/ 
defaultparamsgauge=0 
PARAM_SET=MyCRESTPAR 
ROUTING_PARAM_Set=MyKWPAR 
TIMESTEP=30u 
TIME_BEGIN=202010100830 
TIME_END=202010110400 
```