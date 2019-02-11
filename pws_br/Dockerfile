FROM kapacitor:1.5.1

ENV MBSERVICE_DIR /opt/mb_bre
RUN mkdir -p $MBSERVICE_DIR
COPY requirements/ $MBSERVICE_DIR/requirements/

RUN apt-get update && apt-get install -y \
  git \
  python \
  python-pip \
  python-dev \
  build-essential

RUN pip install -r $MBSERVICE_DIR/requirements/dev.txt
RUN rm -r $MBSERVICE_DIR/requirements/

RUN git clone https://github.com/influxdata/kapacitor.git $MBSERVICE_DIR/kapacitor
RUN cd $MBSERVICE_DIR/kapacitor/udf/agent/py/ && python setup.py install

COPY source/ $MBSERVICE_DIR/source/
COPY tests/ $MBSERVICE_DIR/tests/
COPY config/kapacitor.conf /etc/kapacitor/kapacitor.conf
COPY ./scripts/start_kapacitor /usr/bin/

WORKDIR $MBSERVICE_DIR/source

CMD ["start_kapacitor"]
