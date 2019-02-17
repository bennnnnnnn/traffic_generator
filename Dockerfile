FROM python:3.7-stretch
RUN apt-get update
RUN apt-get install -y xvfb chromedriver libxml2-dev libxslt-dev jq
RUN mkdir -p /usr/src/traffic_generator
WORKDIR /usr/src/traffic_generator
COPY *.py /usr/src/traffic_generator/
COPY start.sh /usr/src/traffic_generator/
COPY requirements.txt /usr/src/traffic_generator/
RUN pip install -r requirements.txt
CMD /usr/src/traffic_generator/start.sh