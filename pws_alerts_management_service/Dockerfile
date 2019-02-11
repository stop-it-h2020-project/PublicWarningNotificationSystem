FROM python:3.6.5-alpine3.7

ENV PROJECT_DIR /opt/pws_alerts_management_service
ENV SOURCE_DIR $PROJECT_DIR/alerts_api

# Adding Python requirements
COPY requirements ./requirements/

# Adding credentials for git cloning
ENV HOME /root
COPY .netrc $HOME/

# Install requirements
RUN apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
     python3 git musl-dev postgresql-dev gcc geos && \
     python3 -m ensurepip && \
     rm -r /usr/lib/python*/ensurepip && \
     pip3 install setuptools && \
     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
     if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
     rm -r /root/.cache

RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt

# Removing credentials and requirements
RUN rm -rf $HOME/.netrc
RUN rm -rf requirements

# Prepare alerts_api and scripts
ENV PROJECT_ROOT $SOURCE_DIR
ENV FLASK_APP=$SOURCE_DIR/main.py

RUN mkdir -p $SOURCE_DIR
COPY scripts /usr/local/bin

COPY alerts_api $SOURCE_DIR/

#  Prepare test artfifacts
COPY scripts $PROJECT_DIR/scripts/
COPY tests $PROJECT_DIR/tests/
COPY pytest.ini $PROJECT_DIR/
RUN mkdir -p $PROJECT_DIR/reports

EXPOSE 5000
WORKDIR $PROJECT_DIR
CMD ["run_api"]
