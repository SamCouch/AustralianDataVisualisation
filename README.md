# Australian Data Visualisation Project

##### To see the final product, download the layermap.html file and run from your files, using a web browser.

The goal of this project was to be able to provide geographic visual data for a client.
This client was a catholic school organisation and can use the data to make better decisions.
These decisions may include, which schools are in likely growth spots and will need more resources, where are good locations to build more schools, and which schools are performing better considering the median weekly income of their neighbourhoods.

Performing this project helped me expand my skills in geographic data skills, in particular in Australia, since most online tools are geared towards America specifically.

To explain the function of the two python scripts in this program, first the filewrite.py script reads the selected csv data files and shapefile from the ABS website and converts it into

The data and shapefile for this project was downloaded from the ABS website at https://datapacks.censusdata.abs.gov.au/datapacks/
Mapshaper which was used to compact the json file can be found here https://mapshaper.org/
The following medium article was also extremely helpful in learning how to use folium https://link.medium.com/s8vm00rZweb

If downloading the project for yourself to create your own map, the filewrite.py file needs to refer to a shapefile. This file was to large to link to directly on github, so it will need to be downloaded and the directory written into the script.
Then, if you wish to compress the map size (which I recommend) make sure that you select 'prevent shape removal' when simplifying the file.
You will also need to manually delete the 'null' geometries as this folium can't handle these, you can find them by searching for 'offshore' in the geojson file and then scrolling to the left. I recommend notepad++ for this. 
You will need to replace these nulls with a 'dummy' shape, I just used a random county from the US from my previous project because it was outside of the map's defines. Here it is below.
{"type": "Polygon", "coordinates": [[[-105.04874, 39.566088], [-104.660626, 39.565909], [-104.662896, 39.129527], [-105.033544, 39.129819], [-105.32922, 39.129689], [-105.260054, 39.210445], [-105.04874, 39.566088]]]} 

If you have any further questions about the project feel free to email me at Samuel.R.Couch@gmail.com
