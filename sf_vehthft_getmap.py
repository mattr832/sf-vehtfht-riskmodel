#!/usr/bin/env python
# coding: utf-8

import folium
from folium import plugins

def get_map(response):
    #initiate the base plot
    folmap = folium.Map([float(response['Latitude']), float(response['Longitude'])], zoom_start=16, width='95%', height='95%')
    folium.Marker(
            location=[float(response['Latitude']), float(response['Longitude'])],
            popup=folium.Popup(html="Risk Score: %s <br> Risk Level: %s <br> Risk Score in 3 Hours: %s <br> Risk Level in 3 Hours: %s" 
                               %(response['Risk Score'],
                                 response['Risk Level'],
                                 response['3+ Hour Risk Score'],
                                 response['3+ Hour Risk Level']),
                              max_width=500),
            icon=folium.Icon(color='green')
    ).add_to(folmap)
    folmap.save('templates/map.html')

