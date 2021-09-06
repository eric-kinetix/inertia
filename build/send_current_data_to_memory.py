from datetime import datetime
import time
from random import randrange
import os
import socket

sensors = ['epoch_time', 'random_number', 'cpu_usage']
sensors = ['epoch_time', 'random_number', 'cpu_usage', 'large_random_number']

hostname = socket.gethostname()

memory_dir = '/dev/shm/'

while True:
    if not os.path.isdir(memory_dir + 'latest'):
        # mode = 0o666
        os.mkdir(memory_dir + 'latest')

    if hostname == 'Erics-Mac-mini':
        host_dir = '/Users/ericmartinez/Dropbox/Kinetix/Product/Inertia/Software'
    else:
        host_dir = '/home/moxa'

    filelist = sorted(os.listdir(host_dir + '/data'))
    filelist.remove('archive')
    try:
        latest_file = host_dir + '/data/' + str(filelist[-1])
    except:
        # print('No Data File Found')
        latest_file = "empty.csv"

    with open(latest_file) as f:
        # first_line = f.readline()
        latest_file_sensors = f.readline().rstrip().split(',')

    with open(latest_file, 'rb') as f:
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b'\n':
            f.seek(-2, os.SEEK_CUR)
        last_line = f.readline().decode()
    latest_file_sensor_values = last_line.rstrip().split(",")

    for idx, sensor in enumerate(latest_file_sensors):
        # print(sensor, latest_file_sensor_values[idx])
        with open(memory_dir + 'latest/' + sensor, 'w') as f:
            f.write(latest_file_sensor_values[idx])
            f.write('\n')

    sleeptime = 1.0 - (time.time() - int(time.time())) + 0.1
    time.sleep(sleeptime)