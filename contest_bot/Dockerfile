FROM python:3

ARG config_path
ENV config_path ${config_path}

ADD run.py /
ADD settings.py /
ADD db_manager.py /
ADD requirements.txt /

RUN pip install -r requirements.txt
#RUN apt-get update
#RUN apt-get -y upgrade

VOLUME /config_path
CMD python3 run.py ${config_path}
