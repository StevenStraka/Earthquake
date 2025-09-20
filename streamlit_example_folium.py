import streamlit as st
import pandas as pd
import plotly.express as px
import json
import os
import folium
import streamlit as st

from streamlit_folium import st_folium
from datetime import datetime, timedelta
import read_earthquake_data_classes as eqc

st.set_page_config(page_title="Steamlit Earthquake Page", page_icon="💰", layout="wide")

url = 'https://earthquake.usgs.gov/earthquakes/feed/v1.0/summary/2.5_day.geojson'


def main():
    st.title("Steamlit Earthquake Page")

    
    earthquakes = eqc.AllEarthquakes(url)
    quakes = []
    for quake in earthquakes.earthquakes:
        quake_tuple = (quake.gid, quake.place, quake.mag, quake.time, quake.title, quake.location.lat, quake.location.lon)
        quakes.append(quake_tuple)

    df = pd.DataFrame(quakes,columns=["id", "Place", "Mag", "Time", "Title", "lat", "lon"])
        
    if df is not None:
        st.dataframe(df)
        m = folium.Map(location=[37.7749, -122.4194], zoom_start=2)
        folium.GeoJson('C:/Progs/Python/Earthquake/TectonicPlateBoundaries.geojson',style_function=lambda feature: {
                "fillColor": "#ffff00",
                "color": "red",
                "weight": 1,
            },).add_to(m)
        
        for quake in earthquakes.earthquakes:
    
            radius = quake.mag * 2.5
            
            timestamp = quake.time/1000
            dt_object = datetime.fromtimestamp(timestamp)
            current_datetime = datetime.now()
            one_hour = timedelta(hours=1)
            time_difference = current_datetime - dt_object

            if time_difference <= one_hour:
                folium.CircleMarker(
                location=[quake.location.lat, quake.location.lon],
                radius=radius,
                color="red",
                stroke=False,
                fill=True,
                fill_opacity=0.99,
                opacity=1,
                popup="{} pixels".format(radius),
                tooltip=quake.title,
                ).add_to(m)
            else:
                folium.CircleMarker(
                location=[quake.location.lat, quake.location.lon],
                radius=radius,
                color="orange",
                stroke=False,
                fill=True,
                fill_opacity=0.75,
                opacity=1,
                popup="{} pixels".format(radius),
                tooltip=quake.title,
                ).add_to(m)
        
        #out = st_folium(m, height=200, return_on_hover=return_on_hover)
        out = st_folium(m, height=850, width=1200)
       
        
main()