#!/bin/bash
CMD="python test.py data/test_x_256.csv 2"
python time_monitor/time_monitor.py -r $LATENCY_REPEAT -o ${RESULT_DIR}/latency_r_${REPEAT}.csv $CMD

