FROM ubuntu:focal

ARG DEBIAN_FRONTEND=noninteractive

RUN apt-get update &&\
    apt-get install -y git curl

RUN echo "APT::Acquire::Retries \"3\";" > /etc/apt/apt.conf.d/80-retries

RUN sed -i 's/archive.ubuntu.com/mirror.enzu.com/' /etc/apt/sources.list
RUN apt-get update && apt-get install -y libllvm10
RUN apt-get install -y cmake g++ libgmp-dev swig python3-numpy
RUN apt-get install -y cmake g++ libboost-all-dev libgmp-dev swig python3-numpy
RUN apt-get install -y python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev
RUN apt-get install -y libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5
RUN apt-get install -y liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins
RUN apt-get install -y python3-zmq python3-scipy python3-gi python3-gi-cairo gobject-introspection gir1.2-gtk-3.0

RUN sed -i 's/mirror.enzu.com/archive.ubuntu.com/' /etc/apt/sources.list

RUN apt-get update && apt-get install -y git cmake g++ libboost-all-dev libgmp-dev swig python3-numpy \
python3-mako python3-sphinx python3-lxml doxygen libfftw3-dev \
libsdl1.2-dev libgsl-dev libqwt-qt5-dev libqt5opengl5-dev python3-pyqt5 \
liblog4cpp5-dev libzmq3-dev python3-yaml python3-click python3-click-plugins \
python3-zmq python3-scipy python3-gi python3-gi-cairo gobject-introspection gir1.2-gtk-3.0

RUN apt-get install -y python3-setuptools

RUN mkdir /sdr

WORKDIR /sdr
RUN git clone https://github.com/EttusResearch/uhd
WORKDIR /sdr/uhd
RUN git checkout v3.15.0.0
WORKDIR /sdr/uhd/host/
RUN mkdir build
WORKDIR /sdr/uhd/host/build
RUN cmake ..
RUN make -j60
RUN make install
RUN ldconfig

RUN uhd_images_downloader 

WORKDIR /sdr
RUN git clone --recursive https://github.com/gnuradio/gnuradio
WORKDIR /sdr/gnuradio
RUN git checkout maint-3.8
RUN git submodule update --init --recursive
RUN mkdir build
WORKDIR /sdr/gnuradio/build
RUN cmake ..
RUN make -j60
RUN make install
RUN ldconfig

RUN gnuradio-config-info --version

WORKDIR /sdr
RUN git clone https://github.com/osmocom/gr-osmosdr
WORKDIR /sdr/gr-osmosdr
#RUN git checkout gr3.7
RUN mkdir build
WORKDIR /sdr/gr-osmosdr/build
RUN cmake ..
RUN make -j60
RUN make install
RUN ldconfig

WORKDIR /sdr
RUN git clone https://github.com/muccc/gr-iridium.git
WORKDIR /sdr/gr-iridium
RUN mkdir build
WORKDIR /sdr/gr-iridium/build
RUN cmake ..
RUN make -j60
RUN make install

RUN ldconfig
WORKDIR /sdr
ENV PYTHONPATH=/usr/local/lib/python3/dist-packages
ENV HOME=/data
WORKDIR /data
