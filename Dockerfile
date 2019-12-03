FROM python:3.8-slim
MAINTAINER Kevin Coakley <kcoakley@sdsc.edu>

ADD . /tmp/install
WORKDIR /tmp/install

RUN pip install -r requirements.txt
RUN ./setup.py install

RUN groupadd -g 999 twitter && \
    useradd -r -u 999 -g twitter twitter

USER twitter

EXPOSE 8000

CMD twitter-stream-archive --debug