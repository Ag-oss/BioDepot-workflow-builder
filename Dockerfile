FROM ubuntu:latest
MAINTAINER lhhung<lhhung@uw.edu>

ENV DEBIAN_FRONTEND noninteractive
ENV HOME /root
#base files/utils to be used inside container
RUN apt-get update \
    && apt-get install -y --force-yes --no-install-recommends supervisor \
        pwgen sudo nano \
        net-tools \
        fluxbox feh xterm x11vnc xvfb \
        gtk2-engines-murrine ttf-ubuntu-font-family \
        fonts-wqy-microhei \
        language-pack-zh-hant language-pack-gnome-zh-hant \
        nginx \
        mesa-utils libgl1-mesa-dri \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
    
#files for  vnc framebuffer
RUN apt-get update && apt-get install -y wget \
    && chdir /tmp \
    && wget 'https://launchpad.net/~fcwu-tw/+archive/ubuntu/ppa/+build/8270310/+files/x11vnc_0.9.14-1.1ubuntu1_amd64.deb' \
    && wget 'https://launchpad.net/~fcwu-tw/+archive/ubuntu/ppa/+files/x11vnc-data_0.9.14-1.1ubuntu1_all.deb' \
    && dpkg -i /tmp/x11vnc*.deb \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/* \
    && chdir /root && rm /tmp/*.deb    

#files for web interface noVNC
ADD web /web/
RUN apt-get update && apt-get install -y docker.io  build-essential gcc python-pip python-dev python3-pip \
    && pip install --upgrade pip \
    && pip install -U setuptools \
    && pip install -r /web/requirements.txt \
    && pip3 install docker \
    && apt-get remove -y gcc build-essential python-pip python-dev python3-pip \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
    
ADD noVNC /noVNC/

#files for orange and biodepot
RUN apt-get update \
    && apt-get install -y --no-install-recommends virtualenv libssl-dev libqt5webkit5-dev python3-pyqt5 python3-pyqt5.qtsvg python3-pyqt5.qtwebkit

RUN rm /bin/sh && ln -s /bin/bash /bin/sh
RUN virtualenv --python=python3 --system-site-packages orange3venv
RUN source orange3venv/bin/activate
#ADD biodepot biodepot
RUN apt-get update && apt-get install -y build-essential gcc git python-dev python3-dev python3-pip python-pip\
    && git clone https://github.com/biolab/orange3.git \
    && pip3 install --upgrade pip \
    && pip install numpy \
    && pip3 install -U setuptools \
    && pip3 install -r orange3/requirements-core.txt \
    && pip3 install -r orange3/requirements-gui.txt \
    && pip3 install docker pysam beautifulsoup4\
    && pip3 install -e orange3 \
#    && apt-get remove -y git gcc build-essential python3-pip python-pip \
    && apt-get remove -y git gcc build-essential \
    && apt-get autoclean -y \
    && apt-get autoremove -y \
    && rm -rf /var/lib/apt/lists/*
    
#nginx and supervisor setup
ADD supervisord.conf /etc/supervisor/conf.d/
ADD nginx.conf /etc/nginx/sites-enabled/default

#json pickle 
RUN pip3 install --user jsonpickle

#put biodepot here and keep pip for rapid updates
ADD biodepot biodepot
RUN pip3 install -e biodepot 

ADD startup.sh /
EXPOSE 6080
WORKDIR /data

#Change app name to Bwb
RUN sed -i 's/\"Orange Canvas\"/\"Bwb\"/' /orange3/Orange/canvas/config.py

#patch orange3
COPY orangePatches/schemeedit.py /orange3/Orange/canvas/document/schemeedit.py

#set up some config files
COPY fluxbox_config/ /root/.fluxbox/
COPY user_config/ /root/

#Add tutorial
COPY tutorials/ /root/tutorials/

#Add widget creator
RUN ln -s /biodepot/orangebiodepot/util/createWidget /usr/bin/createWidget 

#start it up
CMD /startup.sh && /usr/bin/supervisord -n -c /etc/supervisor/supervisord.conf

