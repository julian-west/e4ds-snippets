# Voila Webapp Series

This folder contains the source code for the Voila Webapp Series:
- Part 1: Turn your Jupyter notebook into a webapp
- Part 2: Optimising Voila Webapp Performance (tbc)
- Part 3: Deploy your Voila Webapp on GCP (tbc)

## Getting Started

**Docker (recommended)**

If you are familiar with Docker you can use the `docker-compose` files to build the environments for each web app. For example, run the following command to run the voila web app for Part 1:

```
docker-compose -f part1.docker-compose.yml up --build
```

The Voila application will be available to view at http://localhost:8866

**Virtual Environments**

Alternatively, you can install the required packages within a virtual environment. For example, if you use `conda`:

```
# create environment
conda create -n voila python=3.9 -y

# activate environment
conda activate voila

# run the voila application
voila part1/stock_analysis_eda.ipynb
```
