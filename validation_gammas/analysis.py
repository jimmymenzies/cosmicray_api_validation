import codecs
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import yaml

fig = plt.figure()
ax = fig.add_subplot(111)
energy_label = r'$E \, (MeV)$'
ax.set_xlabel(energy_label)
diff_intensity_label = r"$\frac{d \varphi}{d E} \, (cm^{-2} s^{-1} sr^{-1} MeV^{-1})$"
ax.set_ylabel(diff_intensity_label)

colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Construct the target URL
hostname = "https://cosmicrays.amentum.space/api/get_differential_intensity"

# Requests lets you pass query string params as a dictionary
payload = {
    'particle':'gamma',
    'angle' : '1.0'
}

# This study contains results from experiments on different dates and 
#locations, so other parameters are set in the loop

# Read the experimental data from YAML file
with open('./gamma_cecchini.yaml') as f : 
    doc = yaml.load(f, Loader=yaml.FullLoader)
f.close()

# For each measurement set corresponding to a unique altitude
for i,plot in enumerate(doc['plots']):

    # Analyse and plot the reference data from Cecchini paper
    data = np.array(plot['data'])

    altitude = plot['altitude']['value']

    kes = data.T[0]
    fluxes = data.T[1]

    kes_triplets = kes.reshape(-1,3)
    fluxes_triplets = fluxes.reshape(-1,3)

    kes = [d[1] for d in kes_triplets]
    
    low_fluxes = np.array([d[0] for d in fluxes_triplets])
    mean_fluxes = np.array([d[1] for d in fluxes_triplets])
    high_fluxes = np.array([d[2] for d in fluxes_triplets])

    low_fluxes = mean_fluxes - low_fluxes
    high_fluxes = high_fluxes - mean_fluxes

    plt.errorbar(kes  # MeV
                , mean_fluxes  # /cm2/s/sr/MeV
                , yerr=[low_fluxes, high_fluxes] # ditto
                , linestyle = "None"
                , marker = "s"
                , label = np.str(altitude) + " m"
                , color = colors[i])
    
    # Convert altitude from m to km
    altitude /= 1000.0
    payload['altitude'] = str(altitude)
    
    year = plot['year']
    payload['year'] = str(year)
    
    # month and day are not given in the published data, we assume the 1st of Jan 
    # TODO update if/when further information is provided
    payload['month'] = "1"
    payload['day'] = "1"
    
    latitude = plot['latitude']['value']
    if plot['latitude']['units'] == "S": latitude *= -1.0 
        
    payload['latitude'] = str(latitude)
    
    longitude = plot['longitude']['value']
    if plot['longitude']['units'] == "W": latitude *= -1.0 
        
    payload['longitude'] = str(longitude)
    
    # Hit the Cosmic Ray API and fetch the intensities
    try:
        response = requests.get(hostname, params=payload)
        response.raise_for_status()
    except requests.exceptions.HTTPError as e:  
        print(e)
        sys.exit(1)
    
    json_payload = response.json()

    # Extract the differential energy distribution
    kes = json_payload["energies"]["data"] # MeV
    flux = json_payload["intensities"]["data"] # /cm2/s/sr/MeV
    
    # The API will return energies up to 10GeV, so we crop the data for this comparison
    max_kei = np.searchsorted(kes, 20)# MeV
    
    kes = kes[:max_kei]
    flux = flux[:max_kei]
    
    ax.plot(kes # MeV
        , flux  #
        , linestyle = "-"
        , marker = "None"
        , color = colors[i])

ax.semilogy()
ax.grid()
ax.set_xlim(left = 0, right = 20)# MeV
ax.legend(loc="upper right", fontsize = 'small', numpoints = 1)
plt.tight_layout()
plt.savefig("gamma_cecchini.png")