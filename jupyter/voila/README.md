# Voila Webapp Series

This folder contains the source code for the Voila Webapp Series:
- [Part 1: Voilà! Interactive Python Dashboards Straight from your Jupyter Notebook](https://engineeringfordatascience.com/posts/voila_python_dashboard_part1/)
- Part 2: Optimising Voila Webapp Performance (coming soon)
- Part 3: Deploy your Voila Webapp on GCP (coming soon)

![voila app](./static/convert_to_voila.gif "Voila web application from a notebook")

## Getting Started

**Docker (recommended)**

If you are familiar with Docker you can use the `docker-compose` files to build the environment. For example, run the following command to run the voila web app for Part 1:

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

# install packages
pip install -r requirements.txt

# run the voila application
voila stock_comparison_app.ipynb
```
> Note: you must be running Python 3.9 or higher
