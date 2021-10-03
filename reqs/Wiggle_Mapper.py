#!/usr/bin/env python
# coding: utf-8

# In[1]:


# import required libraries
import pandas as pd    # Read CSV data from Wigle Wifi Capture
import folium          # Mapping Library


# In[2]:


# import CSV file
df = pd.read_csv('./dataset/sample.csv', delimiter = ',', encoding='latin-1', header=1)


# In[3]:


# Verify that files have been successfully imported
df.sample(5)


# In[4]:


# Create A List Of Valid Parameters
valid = []
for rows in df[['MAC', 'SSID', 'AuthMode', 'FirstSeen', 'Channel', 'RSSI', 'CurrentLatitude', 'CurrentLongitude', 'AltitudeMeters', 'AccuracyMeters', 'Type']].values:
    if (rows[10] == 'WIFI'):
        valid.append(rows)                


# In[5]:


# Clean Set by dropping all NA values
validframes = pd.DataFrame(valid).dropna()
validframes.head()


# In[6]:


# Label Columns
validframes.columns = ['MAC', 'SSID', 'AuthMode', 'FirstSeen', 'Channel', 'RSSI', 'CurrentLatitude', 'CurrentLongitude', 'AltitudeMeters', 'AccuracyMeters', 'Type']


# In[7]:


# Compute Average of all the latitudes and longitudes in our dataset to find center and set zoom
# You can also hardcode center adddress like
# mymap = folium.Map( location=[34.0522, -118.243683], zoom_start=12)
mymap = folium.Map( location=[ validframes.CurrentLatitude.mean(), validframes.CurrentLongitude.mean() ], zoom_start=17)


# In[8]:


# Filter Out Wifi Data
for coord in validframes[['CurrentLatitude','CurrentLongitude', 'SSID', 'Type', 'MAC']].values:
    if ("?" not in str(coord[0])) and ("?" not in str(coord[1])):
        # Set location using Lat-Long(cord[0]-cord[1])
        # Set radius and color of marker 
        # Set data to show on popup
        folium.Marker(location=[coord[0],coord[1]],tooltip=["SSID:", coord[2]], popup=["SSID:", coord[2], "BSSID:", coord[4]],icon=folium.Icon(color='red',prefix='fa',icon='wifi')).add_to(mymap)


# In[9]:


# Save MapData To HTML File:
mymap.save('mapdata.html')


# In[12]:


get_ipython().run_cell_magic('HTML', '', '<iframe width="100%" height="650" src="mapdata.html"></iframe>')

