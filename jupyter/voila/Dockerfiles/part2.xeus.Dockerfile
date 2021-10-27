FROM jupyter/base-notebook:python-3.9.7

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

RUN conda install -c conda-forge xeus-python==0.13.3

COPY . /home/jovyan/work/

CMD python -m voila /home/jovyan/work/stock_comparison_app_xeus.ipynb \
    --MappingKernelManager.cull_interval=20 \
    --MappingKernelManager.cull_idle_timeout=20
