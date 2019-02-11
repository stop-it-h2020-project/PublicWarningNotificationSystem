FROM python:3.6-alpine3.4

COPY requirements/ ./requirements

# Add credentials for library cloning, .netrc must exist locally on build-time
ENV HOME /root
COPY .netrc $HOME/

# Install requirements
RUN apk add --update-cache --repository http://dl-3.alpinelinux.org/alpine/edge/testing/ \
    python3 git \
    musl-dev \
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

# Removing credentials
RUN rm -rf $HOME/.netrc
RUN rm -rf requirements/

# Placing code
ENV EMAIL_NOTIFIER_DIR /opt/pws_email_notifier
ENV PROJECT_ROOT $EMAIL_NOTIFIER_DIR/

COPY email_notifier/ $EMAIL_NOTIFIER_DIR/

WORKDIR $EMAIL_NOTIFIER_DIR

# copy tests for make run-tests
COPY tests/ $EMAIL_NOTIFIER_DIR/tests/
COPY .coveragerc pytest.ini $EMAIL_NOTIFIER_DIR/tests/
COPY scripts $EMAIL_NOTIFIER_DIR/scripts/
RUN mkdir -p $EMAIL_NOTIFIER_DIR/reports

CMD [ "python", "connector_main.py" ]
