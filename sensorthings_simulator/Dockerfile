FROM python:3.6.5-alpine3.7

ENV MBCONNECTOR_DIR /opt/mb/
ENV HOME /root

COPY .netrc $HOME/

COPY requirements ./requirements

RUN apk add --no-cache --virtual .build-deps \
                build-base git \
        && pip install -r requirements/dev.txt \
        && find /usr/local \
                \( -type d -a -name test -o -name tests \) \
                -o \( -type f -a -name '*.pyc' -o -name '*.pyo' \) \
                -exec rm -rf '{}' + \
        && runDeps="$( \
                scanelf --needed --nobanner --recursive /usr/local \
                        | awk '{ gsub(/,/, "\nso:", $2); print "so:" $2 }' \
                        | sort -u \
                        | xargs -r apk info --installed \
                        | sort -u \
        )" \
        && apk add --virtual .rundeps $runDeps \
        && apk del .build-deps

# copy scripts
COPY scripts /usr/local/bin

RUN rm -rf $HOME/.netrc
EXPOSE 5050
RUN mkdir -p $MBCONNECTOR_DIR
WORKDIR $MBCONNECTOR_DIR
COPY sensorthings_simulator/ $MBCONNECTOR_DIR/sensorthings_simulator
COPY scripts/ $MBCONNECTOR_DIR/scripts
RUN mkdir -p reports
WORKDIR $MBCONNECTOR_DIR/sensorthings_simulator
CMD ["run"]
