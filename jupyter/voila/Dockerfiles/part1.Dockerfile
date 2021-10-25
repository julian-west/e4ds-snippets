FROM jupyter/base-notebook:python-3.9.7

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

COPY . /home/jovyan/work/

CMD python -m voila /home/jovyan/work/stock_comparison_app.ipynb
