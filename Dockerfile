# docker run -i -t -v /Users/vegasq/Projects/p3ka/html:/root/p3ka/site/ p3ka /root/p3ka/p3ka.py

FROM nginx
MAINTAINER Mykola Yakovliev <vegasq@gmail.com>

LABEL Description="Deploy p3ka.com" Vendor="vegasq" Version="1.0"
RUN DEBIAN_FRONTEND=noninteractive apt-get update
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y git
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y nginx
RUN DEBIAN_FRONTEND=noninteractive apt-get install -y python3 python3-pip python3-dev python3-setuptools
#RUN DEBIAN_FRONTEND=noninteractive git clone https://github.com/Vegasq/peka.git ~/p3ka
COPY src/* /root/p3ka/
RUN chmod +x /root/p3ka/p3ka.py
RUN DEBIAN_FRONTEND=noninteractive pip3 install -r /root/p3ka/requirements.txt

# ENTRYPOINT ["/root/p3ka/p3ka.py"]