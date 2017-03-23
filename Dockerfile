# Invoke with: docker run -d --rm --name aqd aquilon
# --hostname test.example.com if you want to run unit tests

# To get an interactive prompt:
# docker run -i -t --name aqd --rm aquilon /bin/bash -c "/bin/bash"

# Built using the upstream branch in .
# It fails because of the lack of protocols (No module named aqdsystems_pb2)

FROM python:2.7
COPY . aquilon
RUN mkdir -p /var/quattor /var/quattor/logs /var/quattor/aquilondb
WORKDIR aquilon/
RUN pip install --no-cache-dir -r requirements.txt
#RUN python setup.py install
COPY etc/aqd.conf.docker /etc/aqd.conf
ENV AQDCONF=/etc/aqd.conf
#CMD [ "git", "daemon", "--export-all", "--base-path=/var", "/var/quattor/template-king/"]
#CMD [ "python", "sbin/aqd.py" ]
CMD [ "tests/dev_aqd.sh" ]
