FROM python:3
ADD run.py /
ADD settings.py /
ADD db_manager.py /
ADD requirements.txt /
RUN pip install -r requirements.txt
RUN apt-get update
RUN apt-get -y upgrade
CMD ["python3", "run.py"]
