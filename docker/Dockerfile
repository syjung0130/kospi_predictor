FROM ubuntu:16.04

RUN sed -i s/archive.ubuntu.com/ftp.daumkakao.com/g /etc/apt/sources.list
RUN apt-get clean
RUN apt-get update 
RUN apt-get install -y make 
RUN apt-get install -y git unzip 
RUN apt-get install -y wget
RUN apt-get install -y build-essential

# install python3.6
# for use "add-apt-repository command"
RUN apt-get install -y software-properties-common
RUN add-apt-repository ppa:jonathonf/python-3.6
RUN apt-get update
RUN apt-get install -y python3.6
RUN apt-get install -y python3-pip
RUN pip3 install --upgrade pip
RUN pip3 install requests
RUN apt-get install -y python3-bs4

RUN pip3 install virtualenv

# install pandas_datareader
RUN pip3 install pandas-datareader

# Set environment variables
# UBUNTU korean locale
RUN apt-get install -y locales
ENV LANGUAGE=ko_KR.UTF-8 
ENV LANG=ko_KR.UTF-8
RUN locale-gen ko_KR.UTF-8
ENV LC_ALL ko_KR.UTF-8

RUN mkdir -p /workdir/build

# VOLUME /workdir/scrapper
VOLUME /workdir/build

WORKDIR /workdir/build

RUN echo "python3 /workdir/predictor/collector/collector.py" > /workdir/pybuild.sh && chmod +x /workdir/pybuild.sh

CMD ["/bin/bash"]
