# coding=utf-8
import matplotlib

matplotlib.use('Agg')
import matplotlib.pyplot as plt
import numpy as np
import scipy.stats as stats
import csv
from collections import defaultdict
import os

result_dir = 'results/'
latency_result_file_path = 'results/latency_r_100.csv'
throughput_result_prefix = 'results/throughput_'
event_keys = ('instructions', 'cycles', 'branch-misses', 'L1-dcache-load-misses', 'LLC-load-misses',
              'IPC', 'branch_MPKL', 'L1-cache-MPKL', 'LLC-MPKL')


def load_latency_result(file_path):
    result = []
    with open(file_path) as r:
        for l in r.readlines():
            delta = float(l[:-1])
            result.append(delta)
    return result


def plot_latency(save_file):
    x = load_latency_result(latency_result_file_path)
    x.sort()
    x_mean = np.mean(x)
    x_std = np.std(x)
    pdf = stats.norm.pdf(x, x_mean, x_std) / len(x)
    plt.close()
    plt.plot(x, pdf)
    plt.xlabel("time elapsed per run in second")
    plt.title("Latency Benchmark Distribution")
    # plt.show()
    plt.savefig(save_file)
    plt.close()


def load_throughput(x, t):
    result_table = defaultdict(dict)

    def read_throughput_csv(filename):
        with open(filename) as csvfile:
            reader = csv.reader(csvfile)
            for i, row in enumerate(reader):
                if i < 2:
                    continue
                try:
                    timestamp, count, event = float(row[0]), int(row[1]), row[3]
                except ValueError:
                    timestamp, count, event = float(row[0]), 0, row[3]
                yield timestamp, count, event

    # def parse_throughput_csv():

    file_path = throughput_result_prefix + 'x_%d_t_%d.csv' % (x, t)
    for timestamp, count, event in read_throughput_csv(file_path):
        if event in event_keys:
            if timestamp not in result_table[event]:
                result_table[event][timestamp] = count

    def build_matrix(result_table):
        m = np.zeros((len(result_table.values()[0].keys()), len(event_keys) + 1), dtype=np.float)
        m[..., 0] = result_table['instructions'].keys()
        for i, event in enumerate(event_keys[:5]):
            m[..., i + 1] = result_table[event].values()

        # IPC
        m[..., 6] = m[..., 1] / m[..., 2]
        # branch MPKI
        m[..., 7] = m[..., 3] / m[..., 1] * 1000
        m[..., 8] = m[..., 4] / m[..., 1] * 1000
        m[..., 9] = m[..., 5] / m[..., 1] * 1000
        m = m[m[:, 0].argsort()]
        return m

    m = build_matrix(result_table)
    return m


def plot_throughput_IPC_sample(save_file):
    runs = [('X/1_single', 1),
            ('X/4_single', 4),
            ('X/16_single', 16),
            ('X/64_single', 64),
            ('X/256_single', 256),
            ]
    matrix = {}
    fig, ax = plt.subplots(figsize=(9, 3))
    for run_name, x_d in runs:
        matrix[run_name] = load_throughput(x_d, 1)
        # ipc
        ax.plot(matrix[run_name][..., 0], matrix[run_name][..., 6], label=run_name)
    ax.set_xlabel("time since start in seconds")
    ax.set_ylabel("IPC")
    ax.set_title("Throughput IPC on Single Threading")
    ax.legend()
    plt.tight_layout()
    plt.savefig(save_file)
    plt.close()


def plot_for_config(x, t):
    plot_event = ('IPC', 'branch_MPKL', 'L1-cache-MPKL', 'LLC-MPKL')
    fig, ax = plt.subplots(figsize=(9, 3))
    m = load_throughput(x, t)
    for i, e in enumerate(plot_event):
        ax.plot(m[..., 0], m[..., 6 + i], label=e)
    ax.set_xlabel("time since start in seconds")
    ax.set_title("X=%d NUM_THREADS=%d" % (x, t))
    ax.legend()
    plt.tight_layout()
    plt.savefig('plots/thr_x_%d_t_%d.png' % (x, t))
    plt.close()


def throughput_plot_all():

    def get_x_t(file_name):
        # throughput_x_16_t_8
        s = file_name.split('_')
        return int(s[2]), int(s[4][0])

    for result_file in os.listdir(result_dir):
        if not result_file.startswith('throughput'):
            continue
        x, t = get_x_t(result_file)
        plot_for_config(x, t)


if __name__ == '__main__':
    # plot_latency('plots/latency_dist.png')
    # plot_throughput_IPC_sample('plots/throughput_single.png')
    throughput_plot_all()