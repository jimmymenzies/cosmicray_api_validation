import codecs
import json
import matplotlib.pyplot as plt
import numpy as np
import os
import requests
import yaml

# Set up the figures and labels
fig = plt.figure()
ax = fig.add_subplot(111)
energy_label = r'$E \, (MeV)$'
ax.set_xlabel(energy_label)
diff_intensity_label = r"$\frac{d \varphi}{d E} \, (cm^{-2} s^{-1} sr^{-1} MeV^{-1})$"
ax.set_ylabel(diff_intensity_label);
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k',  'navy', 'orange']


hostname = "https://cosmicrays.amentum.space/api/get_differential_intensity"

# The request oackage lets you pass query string params as a dictionary, kewl
payload = {
    'year' : '1998',
    'month' : '5',
    'day' : '28',
    'latitude' : '34.4',
    'longitude' : '-107.6',
    'particle' : 'proton',
    'angle' : '1.0'
}


# Read the experimental data from YAML file
with open('./protons_mocchiuti.yaml') as f : 
    doc = yaml.load(f, Loader=yaml.FullLoader)
f.close()

# For each atmospheric depth in the experimental data, in reverse order
for i,plot in enumerate(doc['plots'][::-1]):

    data = np.array(plot['data'])
    kes = data.T[2] # GeV
    intensities = data.T[4] # /m2/s/sr/GeV
    errors = data.T[5] # /m2/s/sr/GeV
    multipliers = data.T[6] #

    # scale the values by the multiplers to separate the plots in y
    intensities *= multipliers
    errors *= multipliers

    atm_depth = plot['atm_depth']['value']
    this_label = np.str(atm_depth) + plot['atm_depth']['units']
    
    print("atmospheric depth ", this_label)
    
    this_color = colors[i]

    ax.errorbar(kes*1000.0 #GeV-> MeV
        , intensities*1e-7  #/m2/s/sr/GeV -> /cm2/s/sr/MeV
        , yerr = errors*1e-7
        , linestyle = "None"
        , marker = "."
        , label = this_label
        , color = this_color)

    # Over-write the atmospheric depth parameter for this dataset
    payload['atmospheric_depth'] = str(atm_depth)

    # Hit the Cosmic Ray API and fetch the effective dose rate
    try:
        response = requests.get(hostname, params=payload)
    except requests.exceptions.RequestException as e:  
        print(e)
    
    json_payload = response.json()

    # Extract the energy differential flux distribution
    kes = json_payload["energies"]["data"] # MeV
    flux = json_payload["intensities"]["data"] # /cm2/s/sr/MeV

    ax.plot(kes # MeV
        , flux  #
        , linestyle = "-"
        , marker = "None"
        , color = this_color)

# Finalise formatting and save the plot
ax.loglog()
ax.grid()
ax.set_xlim(left = 1e2, right =1e5)
ax.legend(loc="upper right", fontsize = 'small', numpoints = 1)
plt.tight_layout()
plt.savefig("protons_mocchiuti.png")

