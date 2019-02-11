FROM python:3.6.6-alpine

RUN apk add --update \
    python \
    python-dev \
    py-pip \
    build-base \
  && rm -rf /var/cache/apk/*

COPY ./data_generator /opt/pws_br/data_generator

RUN pip install -r /opt/pws_br/data_generator/requirements-dev.txt
RUN rm -r /opt/pws_br/data_generator/requirements-dev.txt

COPY ./data_generator/run.sh /usr/bin/

WORKDIR /opt/pws_br/data_generator
CMD ["run.sh"]
