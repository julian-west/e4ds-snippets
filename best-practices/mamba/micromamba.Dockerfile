FROM ubuntu

RUN wget -qO- <https://micromamba.snakepit.net/api/micromamba/linux-64/latest> | tar -xvj bin/micromamba

RUN ./bin/micromamba shell init -s bash -p ~/micromamba
RUN source ~/.bashrc

RUN micromamba activate
RUN micromamba install --file requirements.txt
