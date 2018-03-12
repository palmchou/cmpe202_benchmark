#!/bin/bash

EVENTS="instructions,cycles,branch-misses,L1-dcache-load-misses,LLC-load-misses"

if [ $# = 0 ]
then
  echo "Missing arguments"
  echo "USAGE: --human_readable    # for readable output from perf"
  echo "       --machine_readable  # for csv outputs"
exit 1
fi
# set default X_LIST if not exist
if [ -z "$X_LIST" ]
then
    X_LIST="1 4 16 64 256"
fi
# set default N_THREAD_LIST if not exist
if [ -z "$N_THREAD_LIST" ]
then
    N_THREAD_LIST="1 2 4 8"
fi

for X in $X_LIST
do
  for n_threads in $N_THREAD_LIST
  do
    echo "benchmarking on input size X / $X with $n_threads threads"
    if [ "$1" = "--human_readable" ]
    then
      perf stat -d python test.py data/test_x_${X}.csv $n_threads
    elif [ "$1" = "--machine_readable" ]
    then
      perf stat -I 1000 -x , -e $EVENTS -o ${RESULT_DIR}/throughput_x_${X}_t_${n_threads}.csv -d python test.py data/test_x_${X}.csv $n_threads
    fi
  done
done

if [ "$1" = "--machine_readable" ]
then
  echo "csv results are saved at $RESULT_DIR"
fi
