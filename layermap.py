# Import Modules
import geopandas as gpd
import pandas as pd
import numpy as np
import folium
import requests
import json
from folium.features import GeoJson, GeoJsonTooltip, GeoJsonPopup
from urllib.request import urlopen

# Read Files
url='https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/geojson/sa2dat.csv'
df=pd.read_csv(url, error_bad_lines=False)
with urlopen('https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/geojson/sa2.json') as response:
    gjs = json.load(response)

# Create Figure
f = folium.Figure(width=680, height=750)

# Define Map
m = folium.Map(
    [-38, 145],
    maxZoom=20,
    minZoom=3,
    zoom_control=True,
    zoom_start=9,
    scrollWheelZoom=True,
    maxBounds=[[0, 90],[-60, 180]],
    dragging=True).add_to(f)

# Define Popup Bubble
popup = GeoJsonPopup(
    fields=['SA2_NAME','STATE_NAME','Pop_Dens','Catholic_Perc','Child_Perc','Median_tot_fam_inc_weekly','Tot_P_P','Median_age_persons','Primary_Cat_Perc',"Secondary_Cat_Perc"],
    aliases=['SA2 Area','State',"Population Density","Catholic Percentage",'Percent Under 5','Median Weekly Family Income',"Population",'Median Age','Percentage Primary Catholic','Percentage Secondary Catholic'],
    localize=True,
    labels=True,
    style="background-color: clear;",
)

# Define Tooltip
tooltip = GeoJsonTooltip(
    fields=['SA2_NAME','Pop_Dens','Catholic_Perc','Child_Perc','Median_tot_fam_inc_weekly'],
    aliases=['SA2 Area',"Population Density",'Catholic Percentage','Percent Under 5','Median Weekly Family Income'],
    localize=True,
    sticky=False,
    labels=True,
    style="""
        background-color: #F0EFEF;
        border: 1px solid black;
        border-radius: 3px;
        box-shadow: 3px;
    """,
    max_width=800,
)

# Define Scales
g0scale = (df['Pop_Dens'].quantile((0,0.05,0.1,0.4,0.6,0.8,0.9,0.93,0.98,1))).tolist()
g1scale = (df['Catholic_Perc'].quantile((0,0.03,0.08,0.15,0.3,0.7,0.85,0.95,0.98,1))).tolist()
g2scale = (df['Child_Perc'].quantile((0,0.05,0.1,0.2,0.4,0.6,0.8,0.9,0.95,1))).tolist()
g3scale = (df['Median_tot_fam_inc_weekly'].quantile((0,0.05,0.1,0.2,0.4,0.6,0.8,0.9,0.95,1))).tolist()


# Add Population Density Choropleth Layer
g0 = folium.Choropleth(
    geo_data=gjs,
    data=df,
    columns=['SA2_MAIN16','Pop_Dens'],
    key_on='feature.properties.SA2_MAIN16',
    fill_color='YlGn',
    fill_opacity=0.714,
    line_opacity=0.4,
    threshold_scale=g0scale,
    legend_name='Population Density (Per SqKm)',
    name='Population Density',
    nan_fill_opacity=0.9,
    highlight=True,).add_to(m)


# Add Percentage Catholic Choropleth Layer
g1 = folium.Choropleth(
    geo_data=gjs,
    data=df,
    columns=['SA2_MAIN16','Catholic_Perc'],
    key_on='feature.properties.SA2_MAIN16',
    fill_color='YlOrRd',
    fill_opacity=0.714,
    line_opacity=0.4,
    threshold_scale=g1scale,
    legend_name='Percentage Catholic',
    name='Percent Catholic',
    show=0,
    nan_fill_opacity=0.9,
    highlight=True,).add_to(m)

# Add Percent Under 5 Choropleth Layer
g2 = folium.Choropleth(
    geo_data=gjs,
    data=df,
    columns=['SA2_MAIN16','Child_Perc'],
    key_on='feature.properties.SA2_MAIN16',
    fill_color='YlGnBu',
    fill_opacity=0.714,
    line_opacity=0.4,
    threshold_scale=g2scale,
    legend_name='Percent Under 5',
    name='Percent Under 5',
    show=0,
    nan_fill_opacity=0.9,
    highlight=True,).add_to(m)

#  Add Median Weekly Family Income Choropleth Layer
g3 = folium.Choropleth(
    geo_data=gjs,
    data=df,
    columns=['SA2_MAIN16','Median_tot_fam_inc_weekly'],
    key_on='feature.properties.SA2_MAIN16',
    fill_color='PuBuGn',
    fill_opacity=0.714,
    line_opacity=0.4,
    threshold_scale=g3scale,
    legend_name='Median Weekly Family Income',
    name='Median Weekly Family Income',
    show=0,
    nan_fill_opacity=0.9,
    highlight=True,).add_to(m)


# Combine components into figure
t=folium.GeoJson(
    gjs,
    style_function=lambda feature: {
        'fillColor': '#ffff00',
        'color': 'black',
        'weight': 0.001,
        'dashArray': '5, 5'},
    popup=popup,
    tooltip=tooltip,
    name='Tooltip and Popup'
    ).add_to(m)
m.keep_in_front(t)

# Add Layer Control Button
folium.LayerControl(position='bottomright',collapsed=0).add_to(m)

# Save to html
f.save("layermap.html")
