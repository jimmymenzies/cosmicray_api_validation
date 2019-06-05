import codecs
import json
import matplotlib.pyplot as plt
import numpy as np
import os 
from scipy import interpolate
import requests
import sys
import yaml

# initialise the figure
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k',  'navy', 'orange']
fig = plt.figure()
ax = fig.add_subplot(111)
ax.set_xlabel(r'Atmospheric Depth $ (g \, cm^{-2})$')
ax.set_ylabel(r"$\frac{d \varphi}{d E} \, (cm^{-2} s^{-1} sr^{-1} MeV^{-1})$");

# Read the experimental data from file
with open('./muons_circella.yaml') as f : 
    doc = yaml.load(f, Loader=yaml.FullLoader)
f.close()

hostname = "https://developer.amentum.space/cosmic-rays/api/get_differential_intensity"

# Include the API key in the request header 
# Head to https://developer.amentum.space/portal for an API key
headers = {
  'Authorization' : os.environ["AMENTUMAPIKEY"]
}

# Requests lets you pass query string params as a dictionary
payload = {
    'year' : '2001',
    'month' : '8',
    'day' : '9',
    'latitude' : '57',
    'longitude' : '-101',
    'particle' : 'mu-',
    'angle' : '1.0'
}

# Each plot/curve corresponds to a separate window of muon energies
for i, plot in enumerate(doc['particles'][0]['plots']):

    this_color = colors[i]

    # Isolate and plot the experimental data for this curve
    depths = np.array(plot['data']).T[0]# g/cm2
    flux = np.array(plot['data']).T[1]# /m2/s/sr/GeV 

    lower_energy = plot['window'][0]# GeV
    upper_energy = plot['window'][1]

    #print('Energy window ', lower_energy, ' ', upper_energy)

    this_label = r"{0}-{1}".format(lower_energy, upper_energy)

    # Each dataset is scaled by a factor for clarity in the plot 
    scaling = np.float(plot['scaling'])

    # Calculate order of magnitude of the scaling factor, as an integer
    scaling_oom = np.int(np.log10(scaling))
    
    # Add the scaling factor to the legend label for this plot
    if scaling_oom > 0 : 
        this_label += r"$\, (\, 10^{})$".format(scaling_oom)

    ax.plot(depths  # g/cm2
        , flux*1e-4*1e-3  # /m2/s/sr/GeV --> /cm2/s/sr/MeV
        , linestyle = "None"
        , marker = "s"
        , label = this_label
        , color = this_color )
    
    # Calculate intensities using the Cosmic Ray API
    # the experimental data is effectively integrated over a range of energies, so
    # we need to do the same for the calculated data
    calc_flux_vs_depth = []
    
    for depth in depths:

        print('Fetching data for depth {} g/cm2'.format(depth))
        
        # Add atmospheric depth to query string params
        payload['atmospheric_depth'] = str(depth)
        
        # Hit the Cosmic Ray API and fetch the energy differential 
        # intensity distribution
        try:
            response = requests.get(hostname, params=payload, headers=headers)
            response.raise_for_status()
        except requests.exceptions.HTTPError as e:  
            print(e)
            sys.exit(1)
            
        json_payload = response.json()

        # Isolate the kinetic energies and fluxes/intensities
        kes_api = json_payload["energies"]["data"] # MeV
        flux_api = json_payload["intensities"]["data"] # /cm2/s/sr/MeV
        
        # Fnd the index of the lower and upper energy limit for this window in the calcuated spectrum
        # ensure the interpolation range is beyond the upper and lower window limits
        li = np.searchsorted(kes_api, lower_energy*1000.0)-1
        ui = np.searchsorted(kes_api, upper_energy*1000.0)+1
        
        # Create 100 linearly spaced kinetic energies in the range of this energy window
        # ensure energies have units of MeV
        kes_lower_edges = np.linspace(np.float(lower_energy)*1000, np.float(upper_energy)*1000, 100)
        e_bin_width = kes_lower_edges[1] - kes_lower_edges[0]
        # Calculate energies in the middle of each bin
        energy_mids = kes_lower_edges + e_bin_width/2.0
        # Drop the last entry as it will fall outside the energy window range
        energy_mids = energy_mids[:-1] 
        
        # Interpolate the flux at the middle of the energy bins 
        f = interpolate.interp1d(kes_api[li:ui], flux_api[li:ui])
        flux_mids = f(energy_mids)
                
        # Integrate between the window limits
        integral_flux = np.trapz(flux_mids, x=energy_mids) # /cm2/s/sr  
        
        # Experimental data is normalised to energy bin width 
        integral_flux /= ((upper_energy - lower_energy)*1000.0)
                        
        calc_flux_vs_depth.append(integral_flux)
    
    calc_flux_vs_depth = np.array(calc_flux_vs_depth)

    ax.plot(depths # MeV
        , calc_flux_vs_depth*scaling  # /cm2/s/sr/MeV
        , linestyle = "-"
        , marker = "."
        , color = colors[i])
    ax.semilogy()

ax.grid()
ax.set_xlim(left = 0, right = 1500)
legend = ax.legend(title="K.E., GeV (scaling)",
    loc="upper right",
    fontsize = 'small',
    numpoints = 1)
plt.setp(legend.get_title(),fontsize='x-small')
plt.savefig("muons_circella.png")