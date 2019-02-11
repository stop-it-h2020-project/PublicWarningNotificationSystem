FROM python:3.6.5-alpine3.7

ENV PWS_RESPONDER_API_DIR /opt/pws_responder_api/

COPY requirements ./requirements/

# adding credentials for git cloning
ENV HOME /root
COPY .netrc $HOME/

# Install requirements
RUN apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
     python3 git \
     musl-dev \
     postgresql-dev \
     gcc \
     geos && \
     python3 -m ensurepip && \
     rm -r /usr/lib/python*/ensurepip && \
     pip3 install setuptools && \
     if [ ! -e /usr/bin/pip ]; then ln -s pip3 /usr/bin/pip ; fi && \
     if [[ ! -e /usr/bin/python ]]; then ln -sf /usr/bin/python3 /usr/bin/python; fi && \
     rm -r /root/.cache
RUN pip install --upgrade pip
RUN pip install -r requirements/dev.txt

# removing credentials
RUN rm -rf $HOME/.netrc
RUN rm -r requirements

RUN mkdir -p $PWS_RESPONDER_API_DIR/source/
WORKDIR $PWS_RESPONDER_API_DIR

# copy scripts
COPY scripts /usr/bin

COPY source $PWS_RESPONDER_API_DIR/source/
ENV PROJECT_ROOT $PWS_RESPONDER_API_DIR/source/

# copy tests
COPY tests $PWS_RESPONDER_API_DIR/tests/
COPY .coveragerc $PWS_RESPONDER_API_DIR/
COPY pytest.ini $PWS_RESPONDER_API_DIR/
COPY scripts $PWS_RESPONDER_API_DIR/scripts/
RUN mkdir -p $PWS_RESPONDER_API_DIR/reports

EXPOSE 5000
WORKDIR $PROJECT_ROOT
CMD ["run"]
