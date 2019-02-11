FROM python:3.6.5-alpine3.7

ENV PROJECT_DIR /opt/pws_external_alerts_management_service
ENV PROJECT_ROOT $PROJECT_DIR
RUN mkdir -p $PROJECT_DIR
COPY requirements $PROJECT_DIR/requirements/

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
RUN pip install -r $PROJECT_DIR/requirements/dev.txt

# Removing credentials and requirements
RUN rm -rf $HOME/.netrc
RUN rm -rf $PROJECT_DIR/requirements

WORKDIR $PROJECT_DIR

# Prepare alerts_api and scripts
COPY pws_external_alerts_management_service/ $PROJECT_DIR/
COPY scripts /usr/bin/

CMD ["run"]