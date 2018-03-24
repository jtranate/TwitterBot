FROM python:3

ARG config_path
ENV config_path ${config_path}
ENV app_path /app

COPY contest_bot ${app_path}

RUN pip install -r ${app_path}/requirements.txt
#RUN apt-get update
#RUN apt-get -y upgrade

VOLUME /config_path
CMD python3 /${app_path}/run.py ${config_path}
