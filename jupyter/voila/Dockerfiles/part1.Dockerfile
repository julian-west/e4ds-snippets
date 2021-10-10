FROM jupyter/base-notebook:python-3.8.8

COPY requirements.txt .

RUN python -m pip install -r requirements.txt

ARG APP_PATH=part1
ENV APP_PATH=${APP_PATH}

COPY $APP_PATH ./$APP_PATH

CMD python -m voila /$APP_PATH/stock_analysis_eda.ipynb
