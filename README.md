# Jabiru API Validation studies

This repository contains validation studies for the JABIRU Cosmic
Ray API at https://amentum.space

Each directory contains:
1. a Jupyter notebook with calls to the API to calculate cosmic ray doses or intensities
2. files (e.g. CSV, YAML) containing published experimental dose or intensity data, and
3. an image of the comparison between calculation and experiment, used as a
thumbnail on the landing page of the API.

## Adding a validation study

Clone the git repository

    git clone https://github.com/amentumspace/jabiru_api_validation.git

Create a new branch

    git checkout -b Study_<study number>

where `<study_number>` increments the current highest study number in the repository.

Create a new directory and change to it

    mkdir Study_<study number>; cd Study_<study number>;

Launch Jupyter and create a new notebook.

    jupyter-notebook

Write Python code that calculates doses or intensities using the API and
plots calculated and experimental data, and saves an image of the
resulting plot. You can based the notebook on those in the existing directories.

Add the files to the repository and write a commit message.     

    git add <jupyter_notebook> <experimental_data_file> <image>

Commit and push the branch to the repository.

    git commit -a -m "A descriptive commit message."
    git push -u origin Study_<study number>

Finally, login to github and create a pull request so we can merge your branch
with the master branch and include a thumbnail to the image on the API landing page.

Copyright 2018 Amentum Aerospace, Australia
