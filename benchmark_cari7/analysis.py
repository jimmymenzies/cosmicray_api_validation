import codecs
import json
import matplotlib.cm as cm
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
import numpy as np
import os
import requests 
import yaml 

# Firstly read the waypoint dataset from the csv file
cari_results = np.loadtxt("./Flight_QF64.DAT", \
    dtype={\
        'names': ('lat', 'long', 'depth', 'step', 'dose rate', 'total dose'), \
        'formats': ('f4', 'f4', 'f4', 'i4', 'f4', 'f4')
    })

# Extract longitudes and latitudes 
longitudes = cari_results['long']
latitudes = cari_results['lat']
# CARI-7 considers longitudes as eastings only. We need to convert to eastings and westings
indices = longitudes > 180 
longitudes[indices] = longitudes[indices] - 360 

# Initialise the map of the world
fig_map = plt.figure(figsize=(8,4.5))
ax_map = fig_map.add_subplot(111)
m = Basemap(llcrnrlon=10., llcrnrlat=-55., urcrnrlon=160., urcrnrlat=10., resolution='l', projection='merc');
m.drawmapboundary(fill_color='#ffffff');
m.drawcoastlines();
#m.fillcontinents();

# Draw waypoints on the map
long, lat = m(longitudes,latitudes)
m.scatter(long, lat, 2, marker='.',color='r', linestyle="-")
# Draw parallels and meridians
m.drawparallels(np.arange(np.min(latitudes),np.max(latitudes),20),labels=[1,1,0,1])
m.drawmeridians(np.arange(-180,180,30),labels=[1,1,0,1])
plt.show;
# Save a jpg to use as a thumbnail
plt.savefig("benchmark_cari7_map.png")

# Initialise the figure for plotting Effective Dose Rates vs waypoint number
fig_dose = plt.figure(figsize=(8,4.5))
ax_dose = fig_dose.add_subplot(111)
ax_dose.set_xlabel("Waypoint #")
ax_dose.set_ylabel("Effective Dose Rate, uSv/hr"); 

# Construct the target URL
hostname = "https://developer.amentum.space/cosmic-rays/api/calculate_dose_rate"

# Requests lets you pass query string params as a dictionary
payload = {
    'year':'2018',
    'month' : '7',
    'day' : '28',
    'particle' : 'total',
    
}
# Append other parameters to the query string to set the date and particle type  

# Include the API key in the request header 
headers = {
  'Authorization' : os.environ['AMENTUMAPIKEY']
}

# Initialise lists to store dose rates 
api_dose_rates = []
cari_dose_rates = []

for step in cari_results:
    cari_dose_rates.append(step['dose rate'])
    
    # Append parameters specific to each waypoint to the target API URL
    payload['latitude'] = np.str(step['lat'])
    
    longitude = step['long']
    if longitude > 180 : longitude -= 360 
        
    payload['longitude'] = np.str(longitude)
        
    payload['atmospheric_depth'] = np.str(step['depth'])
    
    # Hit the Cosmic Ray API and fetch the effective dose rate
    try:
        response = requests.get(hostname, params=payload, headers=headers)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:  
        print(e)
        sys.exit(1)
    
    json_payload = response.json()
    
    dose_rate = json_payload["dose rate"]["value"] # uSv/hr
    
    api_dose_rates.append(dose_rate)

ax_dose.plot(cari_dose_rates  # uSv/hr
    , linestyle = "-"
    , marker = "None"
    , color = "r"
    , label = "CARI-7 (ICRP Rep 106) inside aircraft")

ax_dose.plot(api_dose_rates  # uSv/hr
    , linestyle = "-"
    , marker = "None"
    , color = "b"
    , label = "API (ICRP Rep 116) in atmosphere")

ax_dose.legend(loc="upper left", fontsize = 'small', numpoints = 1);

ax_dose.set_ylim(bottom=0, top=1.3*np.max(cari_dose_rates));
ax_dose.set_xlim(left=0)

plt.savefig("api_cari6.png")
