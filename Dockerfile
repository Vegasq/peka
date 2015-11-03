# docker run  -i -t -v /usr/share/nginx/html/:/root/p3ka/site p3ka /usr/bin/python /root/p3ka/p3ka.py

FROM ubuntu
MAINTAINER Mykola Yakovliev <vegasq@gmail.com>

LABEL Description="Deploy p3ka.com" Vendor="vegasq" Version="1.0"
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python2.7 python-pip python-dev python-setuptools
RUN DEBIAN_FRONTEND=noninteractive easy_install supervisor
RUN DEBIAN_FRONTEND=noninteractive git clone https://github.com/Vegasq/peka.git ~/p3ka
RUN chmod +x /root/p3ka/p3ka.py
RUN DEBIAN_FRONTEND=noninteractive pip install -r /root/p3ka/requirements.txt

ENTRYPOINT ["/root/p3ka/p3ka.py"]