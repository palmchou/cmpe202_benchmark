#!/bin/bash
REPEAT=100
CMD="python test.py data/test_x_256.csv 2"
python time_monitor/time_monitor.py -r $REPEAT -o ${RESULT_DIR}/latency_r_${REPEAT}.csv $CMD

