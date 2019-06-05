# Cosmic Ray API Validation studies

This repository contains validation studies for the Cosmic Ray API available at https://amentum.space

Each directory contains: 

- a README.md file containing a description of the study, summary of findings, and instructions to run the Python code and re-generate the results
- if applicable, files containing published experimental data for validation, or data calculated by alternative models for the purpose of benchmarking
- images comparison density or temperature images or profiles obtained using the Cosmic Ray API alongside experimental results of predictions of other models.

Feel free to add validation study by creating a new branch and submitting a pull request. 

# Running the analysis

See the analysis.py Python script in each directory to see how the Amentum Atmosphere API was used to retrieve cosmic ray quantities, and the Python code to fetch and process validation data from experimental measurements, or benchmarking data from another model.

Then install the necessary Python packages included in the first few lines of the script.

Set the following environment variable to store your API key. Assuming you are using bash shell, this will be:

    export AMENTUMAPIKEY=<your key>

Alternatively you can hard code it in the Python code.

If you do not have an API key, you can signup for a free one [here](https://developer.amentum.space/portal/) 

Then run the script using the following command:

    python analysis.py 

That will produce results as PNG files in the same directory. 

Copyright 2019 Amentum Aerospace, Australia

Copyright 2019 Amentum Aerospace, Australia
