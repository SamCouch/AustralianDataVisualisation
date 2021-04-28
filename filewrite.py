# Import Modules
import pandas as pd
import geopandas as gpd
import json
import numpy as np

# Get urls
url1 = 'https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/SA2/2016Census_G01_AUS_SA2.csv'
url2 = 'https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/SA2/2016Census_G02_AUS_SA2.csv'
url3 = 'https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/SA2/2016Census_G14_AUS_SA2.csv'
url4 = 'https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/SA2/2016Census_G15_AUS_SA2.csv'
url5 = 'https://raw.githubusercontent.com/SamCouch/AustralianDataVisualisation/master/shape/SA2_2016_AUST.shp'
# Read csvs
df_dat1 = pd.read_csv(url1, error_bad_lines=False)
df_dat2 = pd.read_csv(url2, error_bad_lines=False)
df_dat3 = pd.read_csv(url3, error_bad_lines=False)
df_dat4 = pd.read_csv(url4, error_bad_lines=False)



# NOTE THIS MAY NEED TO HAVE SHAPEFILE DIRECTORY ADDED IF DOWNLOADED FROM GITHUB
# Read Shapefile
df_shp = gpd.read_file('shape/SA2_2016_AUST.shp')



# Merge Datafreames
df_plot = df_dat1.filter(['SA2_MAINCODE_2016', 'Tot_P_P','Age_0_4_yr_P','Age_5_14_yr_P','Age_25_34_yr_P','Age_35_44_yr_P'])
df_ali = df_shp.filter(['geometry','SA2_MAIN16'])
df_plot = df_plot.rename(columns={'SA2_MAINCODE_2016': 'SA2_MAIN16'})

df_plot['SA2_MAIN16'] = df_plot['SA2_MAIN16'].astype(int)
df_ali['SA2_MAIN16'] = df_ali['SA2_MAIN16'].astype(int)

df_arg = df_dat2.filter(['SA2_MAINCODE_2016', 'Median_tot_prsnl_inc_weekly', 'Median_tot_fam_inc_weekly','Median_age_persons'])
df_arg = df_arg.rename(columns={'SA2_MAINCODE_2016': 'SA2_MAIN16'})
df_arg['SA2_MAIN16'] = df_arg['SA2_MAIN16'].astype(int)
df_plot = pd.merge(df_plot,df_arg,on='SA2_MAIN16',how='left')

df_arg = df_dat3.filter(['SA2_MAINCODE_2016', 'Christianity_Catholic_P','Christianity_Tot_P'])
df_arg = df_arg.rename(columns={'SA2_MAINCODE_2016': 'SA2_MAIN16'})
df_arg['SA2_MAIN16'] = df_arg['SA2_MAIN16'].astype(int)
df_plot = pd.merge(df_plot,df_arg,on='SA2_MAIN16',how='left')

df_arg = df_dat4.filter(['SA2_MAINCODE_2016','Pre_school_P','Infants_Primary_Catholic_P','Infants_Primary_Tot_P','Secondary_Catholic_P','Secondary_Tot_P'])
df_arg = df_arg.rename(columns={'SA2_MAINCODE_2016': 'SA2_MAIN16'})
df_arg['SA2_MAIN16'] = df_arg['SA2_MAIN16'].astype(int)
df_plot = pd.merge(df_plot,df_arg,on='SA2_MAIN16',how='left')

df_arg = df_shp.filter(['SA2_MAIN16','SA2_NAME','STATE_NAME','AREA_SQKM'])
df_arg['SA2_MAIN16'] = df_arg['SA2_MAIN16'].astype(int)
df_plot = pd.merge(df_plot,df_arg,on='SA2_MAIN16',how='left')

df_plotn = pd.merge(df_ali,df_plot,on='SA2_MAIN16',how='left')


# Create Dependent Values
df_plotn.insert(3, "Pop_Dens", df_plotn.Tot_P_P/df_plotn.AREA_SQKM, True)
df_plotn.insert(3, "Catholic_Dens", df_plotn.Christianity_Catholic_P/df_plotn.AREA_SQKM, True)
df_plotn.insert(3, "Catholic_Perc", 100*df_plotn.Christianity_Catholic_P/df_plotn.Tot_P_P, True)
df_plotn.insert(3, "Christian_Perc", 100*df_plotn.Christianity_Tot_P/df_plotn.Tot_P_P, True)
df_plotn.insert(3, "Toddler_Perc", 100*df_plotn.Age_0_4_yr_P/df_plotn.Tot_P_P, True)
df_plotn.insert(3, "Child_Perc", 100*(df_plotn.Age_0_4_yr_P+df_plotn.Age_5_14_yr_P)/df_plotn.Tot_P_P, True)
df_plotn.insert(3, "Parents_Child_Perc", 100*(df_plotn.Age_0_4_yr_P+df_plotn.Age_5_14_yr_P+df_plotn.Age_25_34_yr_P+df_plotn.Age_35_44_yr_P)/df_plotn.Tot_P_P, True)
df_plotn.insert(3, "Pre_School_Perc", 100*df_plotn.Pre_school_P/df_plotn.Tot_P_P, True)
df_plotn.insert(3, "Primary_Cat_Perc", 100*df_plotn.Infants_Primary_Catholic_P/df_plotn.Infants_Primary_Tot_P, True)
df_plotn.insert(3, "Secondary_Cat_Perc", 100*df_plotn.Secondary_Catholic_P/df_plotn.Secondary_Tot_P, True)
df_plotn.insert(3, "Cat_Child_Index", 100*(df_plotn.Catholic_Perc/100)*(df_plotn.Toddler_Perc/100), True)

# Delete Invalid Numbers
df_plotn=df_plotn.replace([np.inf, -np.inf, np.nan], 0)

# Delete Small Population Values
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Catholic_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Christian_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Toddler_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Child_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Parents_Child_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Primary_Cat_Ratio'] = np.nan
df_plotn.loc[df_plotn['Infants_Primary_Tot_P'] <= 20, 'Primary_Cat_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Secondary_Cat_Ratio'] = np.nan
df_plotn.loc[df_plotn['Secondary_Tot_P'] <= 20, 'Secondary_Cat_Perc'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Secondary_Cat_Ratio'] = np.nan
df_plotn.loc[df_plotn['Tot_P_P'] <= 100, 'Cat_Child_Index'] = np.nan




# Write to GeoJson
df_plotn.to_file("sa2.json", driver='GeoJSON', dropid='True')

# Write to csv
df_plotn=df_plotn.drop(columns='geometry')
df_plotn.to_csv('sa2dat.csv')
