# Background

This study benchmarks the Cosmic Ray API's effective dose rate calculations against the CARI-7 code of the United States Federal Aviation Administration. 

The CSV datafile 'Flight_QF64.DAT' contains a list of Effective Dose Rates calculated by CARI-7 for waypoints of latitude, longitude, and altitude for Flight QF64 from Johannesburg to Sydney on the 28th of July 2018. 

The script overlays the waypoints on a map (see Figure 1), then plots the effective dose rates at these waypoints as calculated by the two codes (see Figure 2). 

Documentation and source code for the CARI-7 code can be found [here](https://www.faa.gov/data_research/research/med_humanfacs/aeromedical/radiobiology/CARI7/)

# Results

![](./gamma_cecchini.png)

**Figure 1**: Waypoints for Flight QF64 from Johannesburg to Sydney on 28th of July 2018

**Figure 2**: Effective Dose Rate for waypoints along the path of Flight QF64 from Johannesburg to Sydney on 28th of July 2018, as calculated by CARI-7 and the Cosmic Ray API.

## Discussion

The increase in Effective Dose Rate mid-flight is due to two factors: 1. The route takes the flight as far south as -47.24 degrees latitude. The intensity of cosmic rays is generally higher towards the poles due to effects of the Earth's magnetic field; there is a concomitant increase in the Effective Dose rate. 2. The altitude is greater mid-flight.

The Effective Dose Rate calculated by the Cosmic Ray API if systematically lower (approx. 20%) than that predicted by CARI-7. Possible reasons include: 1. CARI-7 doses are calculated using an anthropomorphic phantom inside an aircraft, whereas the Cosmic Ray API assumes values in atmosphere; and 2. CARI-7 uses dose conversion coefficients from ICRP Report 106 whereas Cocmic Ray API uses those in ICRP Report 116. The origin of these discrepancies is under investigation and this analysis will be updated as the API evolves.