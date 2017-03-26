# Base image Python 3.6
FROM python:3.6

# Adding all contents to /tmp
ADD . /tmp/

# All of the stuff below is to just get cx_oracle working
RUN apt-get update && apt-get install -y libaio1 libaio-dev
WORKDIR /tmp/instantclient_12_2
RUN ln -s libclntsh.so.12.1 libclntsh.so
RUN ln -s libocci.so.12.1 libocci.so
ENV OCI_HOME=/tmp/instantclient_12_2
ENV OCI_LIB_DIR=/tmp/instantclient_12_2
ENV OCI_INCLUDE_DIR=/tmp/instantclient_12_2/sdk/include
ENV LD_LIBRARY_PATH=/tmp/instantclient_12_2:$LD_LIBRARY_PATH
ENV PATH=/tmp/instantclient_12_2:$PATH
ENV TNS_ADMIN=/tmp/instantclient_12_2/network/admin

WORKDIR /tmp
# Installing all dependencies
RUN pip install -r requirements.txt
WORKDIR /tmp/spring_batch_dashboard

# Running at 0.0.0.0
ENTRYPOINT [ "python", "manage.py", "runserver", "0.0.0.0:8000" ]
EXPOSE 8000