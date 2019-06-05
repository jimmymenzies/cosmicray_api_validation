# A short script to convert a flight path file from .csv to the .DEG format expected by CARI-7

from datetime import datetime
import numpy as np
import time

waypoints = np.genfromtxt("./Flight_QF64.csv", \
    dtype = "i8, S50, S50, S50, S50, f8, f8, f8", \
    names = ['timestamp', 'UTC', 'Callsign', 'Latitude', 'Longitude', 'Altitude', 'Speed', 'Direction'], \
    delimiter = ",")

start_date = datetime.utcfromtimestamp(waypoints[0]['timestamp'])

header = np.str(start_date.month)+"/"+
    np.str(start_date.year)+", "+
    waypoints[0]['Callsign'].decode("utf-8")+"\n"

f = open('Flight_QF64.DEG', 'wb')

f.write(header.encode('utf8'))

header = "DEG MIN N/S DEG MIN E/W FEET TIME(MIN) \n"

f.write(header.encode('utf8'))

start_datetime = datetime.utcfromtimestamp(waypoints[0]['timestamp'])

for wp in waypoints:
    # Calculate time for this waypoint
    datetime = datetime.utcfromtimestamp(wp['timestamp'])
    # Calculate time since last waypoint (will be zero for first one)
    delta_datetime = datetime - start_datetime
    delta_mins = np.int(delta_datetime.seconds/60) # expected by CARI-7
    
    # Get the latitude as a string and remove the quotation mark
    latitude = wp['Latitude'].decode("utf-8").replace('"','')
    # Convert to float and strip the degrees
    lat_degs = np.int(float(latitude))
    # The remainder will be fraction of degree, convert from decimal to minutes
    lat_minsecs = (float(latitude) - lat_degs)*60
    # Determine the bearing, positive lat is North, negative is South
    lat_bear = 'N'
    if lat_degs < 0 : lat_bear = 'S'
        
    # Repeat for longitude
    longitude = wp['Longitude'].decode("utf-8").replace('"','')
    # Convert to float and strip the degrees
    long_degs = np.int(float(longitude))
    # The remainder will be fraction of degree, convert from decimal to minutes
    long_minsecs = (float(longitude) - long_degs)*60
    # Determine the bearing, positive long is East, negative is West
    long_bear = 'E'
    if long_degs < 0 : long_bear = 'W'
        
    entry = np.str(np.abs(lat_degs)) + ", " + np.str(np.abs(lat_minsecs)) + ", " + lat_bear + ", " + \
        np.str(np.abs(long_degs)) + ", " + np.str(np.abs(long_minsecs)) + ", " + long_bear + ", " + \
        np.str(wp['Altitude']) + ", " + np.str(delta_mins) + "\n"
        
    f.write(entry.encode('utf8'))

f.close()