# Cosmic Ray API Validation studies

This repository contains validation studies for the Cosmic Ray API available at https://amentum.space

Each directory contains: 

1. A README.md file containing a description of the study, summary of findings, and instructions to run the Python code and re-generate the results.
2. If applicable, files containing published experimental data for the purpose of validation, or data calculated by alternative models for the purpose of benchmarking.
3. Images comparing calculations obtained using the Cosmic Ray API alongside experimental results or predictions of other models.

Feel free to add a validation study by creating a new branch and submitting a pull request. 

# Running the analyses

See the analysis.py script in each directory to see how the Amentum Cosmic Ray API was used to retrieve cosmic ray quantities, and the Python code that was used to fetch validation data from experimental measurements, or benchmarking data from another model.

Then install the necessary Python packages included in the first few lines of the script using your Python package manager.

Then run the script using the following command:

    python analysis.py 

That will produce results as PNG files in the same directory. 

Copyright 2019 Amentum Aerospace, Australia

