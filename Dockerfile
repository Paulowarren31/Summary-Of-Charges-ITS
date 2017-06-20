FROM ubuntu:16.04
ENV PYTHONUNBUFFERED 1

ENV ORACLE_HOME /opt/oracle/instantclient_12_1
ENV LD_RUN_PATH=$ORACLE_HOME

COPY instantclient/* /tmp/

RUN \
    apt-get update && mkdir -p /opt/oracle && \
    apt-get -y install unzip libaio1 xmlsec1 python-dev && \
    unzip "/tmp/instantclient*.zip" -d /opt/oracle && \
    ln -s $ORACLE_HOME/libclntsh.so.12.1 $ORACLE_HOME/libclntsh.so && \
    pip install --upgrade pip

RUN mkdir /code

WORKDIR /code

ADD requirements.txt /code/

RUN pip install --upgrade pip && \
      pip install -r requirements.txt

EXPOSE 8080

ADD . /code/

CMD python manage.py migrate; ./start.sh
