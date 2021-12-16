FROM continuumio/miniconda3

# install mamba
RUN conda install mamba -n base -c conda-forge

COPY requirements.txt .
RUN mamba install --file requirements.txt
