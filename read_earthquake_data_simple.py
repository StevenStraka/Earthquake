# ## Read and Parse geojson earthquake data from USGS example
# 
# https://earthquake.usgs.gov/earthquakes/ 
# 
# https://earthquake.usgs.gov/earthquakes/map/
# 
# https://earthquake.usgs.gov/earthquakes/feed/v1.0/geojson.php

import requests

#URL for the USGS 2.5+ mag quakes for the last day
url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'

r_data = requests.get(url)
#print(r.status_code)
theJson = r_data.json()
#print(theJson)

print(type(theJson))
print(theJson.keys())
for key in theJson.keys():
    print(f"Key Name: {key} - Type of the value for the key: {type(theJson[key])}")

quake_count = theJson['metadata']['count']
quake_title = theJson['metadata']['title']

print()
print(f"Number of quakes returned: {quake_count}")
print(f"Title: {quake_title}")
print()

for i in range(quake_count):
    quake = theJson['features'][i]
    print((quake['properties']['place']).encode('utf8'))
    print(quake['properties']['mag'])
    print(quake['geometry']['coordinates'][0])
    print(quake['geometry']['coordinates'][1])
    print(quake['geometry']['coordinates'][2])
    print()
