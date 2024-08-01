# AmeliaSWIM

This repository contains the raw dataset download scripts as well as scripts to preprocess and filter the data:

### Amelia: A Large Dataset and Model for Airport Surface Movement Forecasting [[paper](todo)]

[Ingrid Navarro](https://navars.xyz) *, [Pablo Ortega-Kral](https://paok-2001.github.io) *, [Jay Patrikar](https://www.jaypatrikar.me) *, Haichuan Wang,
Zelin Ye, Jong Hoon Park, [Jean Oh](https://cmubig.github.io/team/jean_oh/) and [Sebastian Scherer](https://theairlab.org/team/sebastian/)

*Equal contribution

## Overview

[Amelia-48](https://ameliacmu.github.io/amelia-dataset/) dataset contains the trajectory as well map data. More information is available on the dataset [website](https://ameliacmu.github.io/amelia-dataset/). 


## Processed Data for 10 airports
Pre-processed data (trajectory+map) for 10 airports [list](https://ameliacmu.github.io/amelia-dataset/) can be found at [dataset](https://airlab-share-01.andrew.cmu.edu:9000/amelia-processed/amelia-10.zip)

## Process Data
To process more trajectory data for any of the 48 airports in the [Data Tracker](https://ameliacmu.github.io/amelia-dataset/) for any time after Dec 1 2022, use the following steps:

### Installation

Install and activate the environment:
```bash
conda env create -f environment.yml
conda activate swim
```
### Download raw files:

The raw SWIM SMES `.njson.gz` files can be downloaded using the following scripts:

```
python download_raw.py 
```
#### Options:

```
  -h, --help            show this help message and exit
  --endpoint ENDPOINT   MinIO server endpoint
  --bucket BUCKET       Name of the bucket to download files from
  --start_time START_TIME
                        Start time in the format YYYY-MM-DD HH:MM:SS (default: 2023-01-01 00:00:00)
  --end_time END_TIME   End time in the format YYYY-MM-DD HH:MM:SS (default: 2023-01-02 00:00:00)
  --destination DESTINATION
                        Local directory to save the downloaded files
```



### Process Data

```
python process.py data=<insert month> airports=<airport ICAO>
```

For example; if you would like to process the data for KSEA for Jan 2023
```
python process.py data=jan airports=ksea
```

#### Options:

In `conf/data/base` the following options exist:


- datapath: #Base Path for Raw Data
- outpath: #Base Path for Processed Data
- window: #Time (in sec) Duration for each CSV
- n_jobs: #Num cpus to use
- parallel: #Use parallel processing
- download: #Download the Raw Data (set to false if you already have the raw data)
- start_time:  #utc linux start time 
- end_datetime:  #utc linux end time 

In `conf/airports/<airport ICAO>` the following options exist:


- airport: #Name of the airport
- ref_lat: #Ref latitude to calculate  x,y cartesian
- ref_lon: #Ref longitude to calculate  x,y cartesian
- max_alt: #Max agent altitude to filter
- fence: #Geo-fence to filter data

#### Available combinations:
```
airports: katl, kaus, kbdl, kbfi, kbna, kbos, kbwi, kcle, kclt, kcvg, kdab, kdal, kdca, kden, kdfw, kdtw, kewr, kfll, khou, khwd, kiad, kiah, kjfk, klas, klax, klga, kmci, kmco, kmdw, kmem, kmia, kmke, kmsp, kmsy, koak, kord, korl, kpdx, kphl, kphx, kpit, kpvd, kpwk, ksan, ksdf, ksea, ksfo, ksjc, kslc, ksna, kstl, kteb, panc, phnl
```
```
data: apr, aug, base, dec, default, feb, jan, jul, jun, mar, may, nov, oct, sep
```
<hr>

## BibTeX

If you find our work useful in your research, please cite us!

```bibtex
@article{navarro2024amelia,
  title={Amelia: A Large Model and Dataset for Airport Surface
Movement Forecasting},
  author={Navarro, Ingrid and Ortega-Kral, Pablo and Patrikar, Jay, and Haichuan, Wang and Park, Jong Hoon and Oh, Jean and Scherer, Sebastian},
  journal={arXiv preprint arXiv:2309.08889},
  year={2024}
}
```