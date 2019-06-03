FROM python:3.6

RUN export TMPDIR=/home/$USER/tmp

RUN pip install \
        numpy \
        tensorflow==1.12.0 \
        pandas \
        tensorflow-serving-api \
        flask \
        requests

# show python logs as they occur
ENV PYTHONUNBUFFERED=0

# add project files
RUN mkdir /home/data/
ADD data/*.csv /home/data/
ADD *.py /home/
ADD templates/* /home/templates/
ADD static/styles /home/static/styles/
RUN mkdir /home/static/tmp/
ADD static/scripts/ /home/static/scripts/

# start server on port 5000
WORKDIR /home/
EXPOSE 5000
ENTRYPOINT python flask_server.py
