import time

import psutil
import nvidia_smi
import socket
import math

HOST = '192.168.0.28'
PORT = 41624

nvidia_smi.nvmlInit()
handle = nvidia_smi.nvmlDeviceGetHandleByIndex(0)


# converts a floating point number of the range 0..1 to a whole number of the range 0..255
def to_byte(fp):
    return min(round(fp * 256), 255)


def per_cpu_usage(interval=1.0):
    return [n / 100 for n in psutil.cpu_percent(interval=interval, percpu=True)]


def mem_usage():
    mem = psutil.virtual_memory()._asdict()
    return mem['used'] / mem['total']


def gpu_usage():
    return nvidia_smi.nvmlDeviceGetUtilizationRates(handle).gpu / 100


def gpu_mem_usage():
    return nvidia_smi.nvmlDeviceGetUtilizationRates(handle).memory / 100


def main_disk_usage():
    usage = psutil.disk_usage('/')
    return usage.used / usage.total


def all_usages():
    return per_cpu_usage() + [mem_usage(), gpu_usage(), gpu_mem_usage(), main_disk_usage()]


def connect_and_feed():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        print('Connecting to host...')
        s.connect((HOST, PORT))
        print('Connected.')
        while True:
            usages = bytes([to_byte(b) for b in all_usages()])
            for usage in usages:
                s.sendall(usages)


while True:
    try:
        connect_and_feed()
    except:
        print('Error, restarting in 5 seconds...')
        time.sleep(5)
