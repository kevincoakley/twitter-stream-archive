FROM python:3.8-slim
MAINTAINER Kevin Coakley <kcoakley@sdsc.edu>

ADD . /tmp/install
WORKDIR /tmp/install

RUN pip install -r requirements.txt
RUN ./setup.py install

CMD twitter-stream-archive --debug