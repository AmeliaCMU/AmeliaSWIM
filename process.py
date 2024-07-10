
from hydra.utils import instantiate
import hydra
import logging
from omegaconf import DictConfig, OmegaConf
import gzip
from geographiclib.geodesic import Geodesic
import os
from glob import glob
import json
import xml.etree.ElementTree as ET
from collections import defaultdict
import pandas as pd
import datetime
import copy
from tqdm import tqdm
import numpy as np
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon
import re
from joblib import Parallel, delayed
import warnings
warnings.filterwarnings("ignore")
from RawDataGrabber import download
from download_raw import MinioFileDownloader

log = logging.getLogger(__name__)

# Define a custom function to apply np.unwrap with NaN values retained


def unwrap_with_nans(arr):
    non_nan_indices = ~np.isnan(arr)  # Get indices of non-NaN values
    # Apply np.unwrap to non-NaN values
    unwrapped = np.unwrap(arr[non_nan_indices])
    # Replace non-NaN values with unwrapped values
    arr[non_nan_indices] = unwrapped
    return arr

def new_column_value(row):
    if pd.isna(row):
        return '[INT]'
    else:
        return '[ORG]'

class Data:

    def __init__(self, cfg: DictConfig) -> None:
        print(OmegaConf.to_yaml(cfg))
        self.cfg = cfg
        self.path = cfg.data.datapath
        self.outpath = cfg.data.outpath
        self.ref_lat = cfg.airports.ref_lat
        self.ref_lon = cfg.airports.ref_lon
        self.max_alt = cfg.airports.max_alt  # ft
        # movement area
        fence = np.array(cfg.airports.fence)

        lons_lats_vect = np.column_stack(
            (fence[:, 1], fence[:, 0]))  # Reshape coordinates
        self.polygon = Polygon(lons_lats_vect)  # create polygon
        self.airport = cfg.airports.airport
        self.geod = Geodesic.WGS84
        self.fields = ['ID', 'datetime', 'Time', 'Date', 'Altitude',
                       'Speed', 'Heading', 'Lat', 'Lon', 'Range', 'Bearing', 'Type','Interp']
        self.data = []

        # download the raw data
        if cfg.data.download:
            downloader = MinioFileDownloader()
            downloader.download_files(cfg.data.start_time-3700,cfg.data.end_datetime+3700,self.path,time_format="unix") ##some constant padding

        if not os.path.exists(self.outpath):
            os.makedirs(self.outpath)
            
        self.filelist = [y for x in os.walk(
            self.path) for y in glob(os.path.join(x[0], 'ALL*.gz'))]
        to_sort = [(re.search('ALL(.*).njson.gz', f).group(1)[2:], f)
                   for f in self.filelist]
        self.sorted_filelist = sorted(to_sort, key=lambda tup: tup[0])
        if "start_time" in cfg.data:
            self.start_time = cfg.data.start_time
        else:
            self.start_time = int(self.sorted_filelist[0][0])

        if "end_datetime" in cfg.data:
            self.end_datetime = cfg.data.end_datetime
        else:
            self.end_datetime = int(self.sorted_filelist[-1][0]) - 1800

        self.end_time = self.start_time + self.cfg.data.window  # 60 MIN moving Window
        self.count = 1
        log.info("Total process from %s to %s", datetime.datetime.fromtimestamp(self.start_time).strftime(
            '%c'), datetime.datetime.fromtimestamp(self.end_datetime).strftime('%c'))

    def read_file(self, t, filename):
        data = []
        try:
            with gzip.open(filename, 'r') as f:
                log.info("Processing: %s %s", filename,
                        datetime.datetime.fromtimestamp(int(t)).strftime('%c'))

                for line in f:
                    obj = json.loads(line)
                    myroot = ET.fromstring(obj['body'])
                    if myroot[0].text == self.airport:
                        for x in myroot.findall("positionReport"):
                            k = (x.find("stid").text)
                            self.pos = defaultdict(lambda: defaultdict())

                            self.pos[k]["ID"] = k
                            # self.pos[k]["Full"] = x.attrib['full'] == 'true'
                            if x.find('position') is not None:
                                if x.find("position").find("latitude") is not None:
                                    self.pos[k]["Lat"] = float(
                                        x.find("position").find("latitude").text)

                                if x.find("position").find("longitude") is not None:
                                    self.pos[k]["Lon"] = float(
                                        x.find("position").find("longitude").text)

                                if x.find("position").find("altitude") is not None:
                                    self.pos[k]["Altitude"] = float(
                                        x.find("position").find("altitude").text)

                            if x.find("movement") is not None:

                                if x.find("movement").find("speed") is not None:
                                    self.pos[k]["Speed"] = float(
                                        x.find("movement").find("speed").text)
                                if x.find("movement").find("heading") is not None:
                                    self.pos[k]["Heading"] = float(
                                        x.find("movement").find("heading").text)

                            if x.find("flightInfo") is not None:
                                if x.find("flightInfo").find("tgtType") is not None:
                                    if x.find("flightInfo").find("tgtType").text == "aircraft":
                                        self.pos[k]["Type"] = 0
                                        # self.pos[k]["Type"] = 3
                                    elif x.find("flightInfo").find("tgtType").text == "vehicle":
                                        self.pos[k]["Type"] = 1

                            stamp = x.find("time").text
                            utc_time = datetime.datetime.strptime(
                                stamp, "%Y-%m-%dT%H:%M:%S.%fZ")
                            self.pos[k]["Time"] = utc_time.strftime("%H:%M:%S.%f")
                            self.pos[k]["Date"] = utc_time.strftime("%m/%d/%Y")
                            self.pos[k]["datetime"] = utc_time

                            # if self.pos[k]["Lat"] and self.pos[k]["Lon"]:
                            # self.pos[k]["Range"], self.pos[k]["Bearing"] = self.get_range_and_bearing(self.ref_lat,self.ref_lon,self.pos[k]["Lat"],self.pos[k]["Lon"])
                            data.append(copy.deepcopy(self.pos[k]))
        except:
            print("File Corrupt!")
        return data

    def process_data(self):
        while self.end_datetime - self.start_time >= 100:
            log.info("Currently processing from %s to %s", datetime.datetime.fromtimestamp(
                self.start_time).strftime('%c'), datetime.datetime.fromtimestamp(self.end_time).strftime('%c'))
            if not os.path.exists(self.outpath + "/" + self.airport + "_" + str(self.count) + "_" + str(self.start_time) + '.csv'):
                filtered_filelist = [i for i in self.sorted_filelist if int(
                    i[0]) > self.start_time-3700 and int(i[0]) < self.end_time + 100]
                log.info("Num Files: %s", len(filtered_filelist))
                # print(filtered_filelist)
                if len(filtered_filelist) < 5:
                    log.error("Error:  Skipping: Num files less than 5")
                    self.start_time = self.start_time + self.cfg.data.window
                    self.end_time = self.end_time + self.cfg.data.window
                    continue
                if self.cfg.data.parallel == True:
                    results = Parallel(n_jobs=self.cfg.data.n_jobs)(
                        delayed(self.read_file)(t, i) for t, i in filtered_filelist)
                    self.data = [
                        item for sublist in results for item in sublist]
                else:
                    self.data = []
                    for t, filename in tqdm(filtered_filelist):
                        log.info("Processing: %s %s ", filename, datetime.datetime.fromtimestamp(
                            int(t)).strftime('%c'))
                        self.data.append(self.read_file(t, filename))

                if len(self.data) == 0:
                    # add data gabber here
                    log.error("Error:  No data")
                    self.start_time = self.start_time + self.cfg.data.window
                    self.end_time = self.end_time + self.cfg.data.window
                    continue
                df = pd.DataFrame(self.data, columns=self.fields)
                # df.to_csv('raw.csv') # save a ckpt csv for testing
                df['datetime'] = pd.to_datetime(df['datetime'])
                df.index = df['datetime']
                del df['datetime']
                # del df['Date']
                # del df['Time']
                df = df.sort_values(by="datetime")

                # interpolation
                df = df.groupby('ID').resample('S').mean()
                
                df['Interp'] = df['Lat'].apply(new_column_value)


                # df.to_csv('test_after_groupby.csv') # save a ckpt csv for testing

                df["Heading"] = np.deg2rad(df['Heading'])

                df['Heading'] = df.groupby('ID')['Heading'].transform(
                    unwrap_with_nans)  # handle unwrapping with NaNs

                df["Heading"] = np.rad2deg(df['Heading'])

                for field in ['Altitude', 'Speed', 'Heading', 'Type','Lat','Lon']:
                    df[field] = df[field].groupby('ID').apply(
                        lambda group: group.interpolate(limit_direction="both"))

                for field in ['Lat', 'Lon']:
                    df[field] = df[field].groupby('ID').apply(
                        lambda group: group.interpolate(limit_direction="both",limit=10))
                    
                for field in ['Altitude', 'Speed', 'Heading', 'Lat', 'Lon']:
                    df[field] = df[field].groupby('ID').apply(
                        lambda group: group.rolling(5, min_periods=1, center=True).mean())

                df['Heading'] %= 360  # Angle Wrap
                # df.to_csv('test_after_interpolation.csv') # save a ckpt csv for testing

                df[['Range', 'Bearing']] = df.apply(lambda row: self.get_range_and_bearing(
                    self.ref_lat, self.ref_lon, row['Lat'], row['Lon']), axis=1, result_type='expand')

                df["Type"].fillna(2, inplace=True)
                # df.to_csv('test_after_fillna.csv') # save a ckpt csv for testing
                df = df.dropna()
                # df.to_csv('test_after_dropna.csv') # save a ckpt csv for testing

                df.reset_index(level=0, inplace=True)

                # geo filters
                df = df[df["Altitude"] < self.max_alt]
                df["geometry"] = [Point(xy)
                                  for xy in zip(df['Lon'], df['Lat'])]
                df["geometry"] = df["geometry"].apply(self.polygon.contains)
                df = df[df["geometry"] == True]
                del df["geometry"]
                df = df.sort_values(by="datetime")

                # additional cols for traj pred compatibility
                df = df.assign(x=lambda x: (x['Range'] * np.cos(x["Bearing"])))
                df = df.assign(y=lambda x: (x['Range'] * np.sin(x["Bearing"])))

                df["time"] = df.index
                first = df["time"].iloc[0]
                df["Frame"] = (df["time"]-first).dt.total_seconds()
                df["Frame"] = df["Frame"].astype("int")
                del df["time"]
                cols = list(df.columns)
                cols = [cols[-1]] + cols[:-1]
                df = df[cols]
                # df_sorted.to_csv(self.outpath + self.airport + "_" + str(self.count) + '.csv.gz', index=False, compression='gzip')
                start = datetime.datetime.fromtimestamp(
                    self.start_time, tz=datetime.timezone.utc)
                end = datetime.datetime.fromtimestamp(
                    self.end_time, tz=datetime.timezone.utc)
                df = df.loc[pd.to_datetime(start):pd.to_datetime(end)]
                if df.empty:
                    print('Error: DataFrame is empty!')
                    self.start_time = self.start_time + self.cfg.data.window
                    self.end_time = self.end_time + self.cfg.data.window
                    continue
                df["Frame"] = df["Frame"] - df["Frame"].iloc[0]
                df.to_csv(self.outpath + "/" + self.airport + "_" +
                          str(self.count) + "_" + str(self.start_time) + '.csv', index=False)
            else:
                print("Found!")
            self.start_time = self.start_time + self.cfg.data.window
            self.end_time = self.end_time + self.cfg.data.window

            self.count += 1

            # data = data.split('

    def get_range_and_bearing(self, lat1, lon1, lat2, lon2):

        lat2 = float(lat2)
        lon2 = float(lon2)
        g = self.geod.Inverse(lat1, lon1, lat2, lon2)

        return g['s12']/1000.0, np.deg2rad(g['azi1'])


@hydra.main(version_base=None, config_path="conf", config_name="config")
def start(cfg: DictConfig) -> None:
    data = Data(cfg)
    data.process_data()


if __name__ == '__main__':

    start()

    log.info("Success!!")
