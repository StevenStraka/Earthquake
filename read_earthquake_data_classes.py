"""
Read and Parse geojson earthquake data from USGS example
https://earthquake.usgs.gov/earthquakes/
https://earthquake.usgs.gov/earthquakes/map/
https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php
"""
from typing import Dict
import requests
import datetime
from dataclasses import dataclass
from pprint import pprint
import sys

#sys.stdout.reconfigure(encoding='utf-8')

# URL for the USGS 2.5+ mag quakes for the last day  (Default for no arg.)
URL = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'


@dataclass
class Location:
    '''Location data info for a single earthquake'''
    lat: float
    lon: float
    depth: float


@dataclass
class Earthquake:
    '''Complete data info for a single earthquake'''
    gid: str
    place: str
    location: Location
    mag: float
    time: int
    title: str


class AllEarthquakes():
    '''All quake data'''

    def __init__(self, url=URL):

        self._url = url
        self.quake_cnt = 0
        self.earthquakes = []
        self.fetch_earthquake_data()

    def fetch_earthquake_data(self) -> None:
        """
        Populate earthquake data
        """
        r_data = requests.get(self._url)
        the_json = r_data.json()
        # print(the_json)
        # print('-'*40)
        # pprint(the_json)
        self.quake_cnt = the_json['metadata']['count']

        for quake in range(self.quake_cnt):
            the_quake = the_json['features'][quake]
            the_location = self.create_location(the_quake)
            self.earthquakes.append(Earthquake(
                the_quake['id'],
                the_quake['properties']['place'],
                the_location,
                the_quake['properties']['mag'],
                the_quake['properties']['time'],
                the_quake['properties']['title']))

    def create_location(self, current_quake) -> Location:
        '''Helper function to create a location object'''

        location = Location(
            current_quake['geometry']['coordinates'][1],
            current_quake['geometry']['coordinates'][0],
            current_quake['geometry']['coordinates'][2])

        return location

    # def find_largest_earthquake(self, debug=False):
    #     max_index = 0
    #     qmax = 0
    #     for index, quake in enumerate(self.earthquakes):
    #         if quake.mag > qmax:
    #             qmax = quake.mag
    #             max_index = index
    #     if debug:
    #         print(qmax, max_index, len(self.earthquakes))
    #     return self.earthquakes[max_index]

    def find_largest_earthquake(self) -> float:
        '''Find quake with largest magnitude'''

        return max(self.earthquakes, key=lambda item: item.mag)

    def get_earthquakes_coords_dict(self) -> Dict:
        quake_lats = []
        quake_lons = []
        quake_depths = []
        for quake in self.earthquakes:
            quake_lats.append(quake.location.lat)
            quake_lons.append(quake.location.lon)
            quake_depths.append(quake.location.depth)

        return dict(lat=quake_lats, lon=quake_lons, depth=quake_depths)

    def list_all_earthquakes(self) -> None:
        for quake in self.earthquakes:
            print(quake.title)

    def list_earthquakes_by_mag(self) -> None:
        sorted_list = sorted(self.earthquakes, key=lambda x: x.mag)
        for quake in sorted_list:
            print(quake.title)

    def list_earthquakes_by_time(self) -> None:
        sorted_quakes = sorted(self.earthquakes, reverse=True, key=lambda x: x.time)
        for quake in sorted_quakes:
            # print(quake.title, quake.time)
            print(quake.title, datetime.datetime.fromtimestamp(int(quake.time/1000)))
    

#     Main Processing....
if __name__ == '__main__':

    def process_quakes(debug: bool) -> None:

        earthquakes = AllEarthquakes()
        print("Total number of earthquakes: {}".format(earthquakes.quake_cnt))
        print("---------------------------")
        earthquakes.list_all_earthquakes()
        print("---------------------------")
        earthquakes.list_earthquakes_by_mag()
        print("---------------------------")
        earthquakes.list_earthquakes_by_time()
        print("---------------------------")

        earthquake = earthquakes.find_largest_earthquake()

        print(earthquake.place)
        print(earthquake.location.lat)
        print(earthquake.location.lon)
        print(earthquake.location.depth)

        if(debug):
            data = earthquakes.get_earthquakes_coords_dict()
            klat, klon, kdepth = data.keys()
            lat, lon, depth = data.values()

    # Process the daily earthquakes
    process_quakes(True)
