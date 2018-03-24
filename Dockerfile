FROM python:3

ENV CONFIG_PATH /config
ENV APP_PATH /app

COPY contest_bot ${APP_PATH}

RUN apt-get update
RUN apt-get -y upgrade
RUN pip install -r ${APP_PATH}/requirements.txt

VOLUME ${CONFIG_PATH}
CMD python3 /${APP_PATH}/run.py ${CONFIG_PATH} ${APP_PATH}
