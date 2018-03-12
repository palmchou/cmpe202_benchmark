FROM gcr.io/tensorflow/tensorflow

RUN apt-get update -y \
  && apt-get install -y git

# dependencies and configurations
RUN apt-get install -y linux-tools-common linux-tools-generic linux-tools-`uname -r` \
  && apt-get install -y python-tk python-pip
RUN pip install matplotlib tqdm numpy==1.13.0

ENV TF_CPP_MIN_LOG_LEVEL 3

RUN mkdir /benchmark
WORKDIR /benchmark

# using perf only, abandon pmu-tools
# download and setup pmu-tools
# RUN git clone https://github.com/andikleen/pmu-tools
# RUN export PATH=$PATH:/benchmark/pmu-tools
# ENV PATH $PATH::/benchmark/pmu-tools

# clone forked project repo 
# original repo: https://github.com/Kyubyong/sudoku
# the forked one provides datasets with suitable size and it's configurable with thread number
RUN git clone https://github.com/palmchou/sudoku.git
WORKDIR /benchmark/sudoku

# add pretrained model
ADD http://shuaizhou.me/files/cmpe202/logdir.tar.gz /benchmark/sudoku/
RUN tar -zxvf logdir.tar.gz
#ADD logdir.tar.gz /benchmark/sudoku/

RUN git clone https://github.com/palmchou/time_monitor.git

ENV RESULT_DIR /benchmark/results
RUN mkdir -p $RESULT_DIR

COPY run_throughput.sh ./
COPY run_latency.sh ./
COPY run_all.sh ./

# run bash to let the container idle
CMD bash 
