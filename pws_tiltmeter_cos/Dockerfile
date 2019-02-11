FROM worldsensing/mbconnector-base:0.0.7-python3.6-alpine3.4

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
COPY scripts /usr/bin

RUN rm -rf $HOME/.netrc
EXPOSE 5050
RUN mkdir -p $MBCONNECTOR_DIR
WORKDIR $MBCONNECTOR_DIR
COPY mbc_pws_sensor_cos/ $MBCONNECTOR_DIR/mbc_pws_sensor_cos
COPY tests/ $MBCONNECTOR_DIR/tests
COPY scripts/ $MBCONNECTOR_DIR/scripts
COPY metadata/ $MBCONNECTOR_DIR/metadata
RUN mkdir -p reports
COPY pytest.ini $MBCONNECTOR_DIR/
WORKDIR $MBCONNECTOR_DIR/mbc_pws_sensor_cos
CMD ["run"]
