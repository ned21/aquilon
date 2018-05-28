# Invoke with: docker run --hostname test.example.com --rm --name aqd aquilon
# --hostname test.example.com is required to run unit tests

# To get an interactive prompt:
# docker run -i -t --name aqd --rm aquilon /bin/bash -c "/bin/bash"

# Before building, you need to:
# git clone https://github.com/quattor/aquilon-protocols.git

FROM centos:7
COPY qwg-external.repo /etc/yum.repos.d/

RUN yum install --nogpgcheck -y ant-apache-regexp ant-contrib \
  gcc git git-daemon java-1.8.0-openjdk-devel libxslt libxml2 make panc \
  knc krb5-workstation \
  protobuf-compiler protobuf-devel \
  python-devel python-setuptools \
  sqlite python-virtualenv
RUN virtualenv --prompt="(aquilon) " /var/quattor/aquilon-venv ; \
  . /var/quattor/aquilon-venv/bin/activate ; \
  pip install --upgrade setuptools ; \
  pip install coverage ; \
  pip install functools32 ; \
  pip install ipaddress ; \
  pip install lxml ; \
  pip install mako ; \
  pip install jsonschema ; \
  pip install psycopg2 ; \
  pip install protobuf ; \
  pip install python-cdb ; \
  pip install python-dateutil ; \
  pip install pyyaml ; \
  pip install six ; \
  pip install sqlalchemy ; \
  pip install twisted
COPY . aquilon
COPY externals/aquilon-protocols protocols
RUN . /var/quattor/aquilon-venv/bin/activate ; cd protocols ; ./setup.py install
RUN mkdir -p /var/quattor /var/quattor/logs /var/quattor/aquilondb
WORKDIR aquilon/
COPY etc/aqd.conf.docker /etc/aqd.conf
#ENV AQDCONF=/etc/aqd.conf # Don't set this for unit tests
ENV KRB5CCNAME=FILE:/tmp/tgt
CMD [ ". /var/quattor/aquilon-venv/bin/activate" "tests/dev_aqd.sh" ]
