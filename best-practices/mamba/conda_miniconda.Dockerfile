FROM continuumio/miniconda3

COPY requirements.txt .
RUN conda install --file requirements.txt
