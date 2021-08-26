from datetime import datetime
import time
from random import randrange
import os
import socket

sensors = ['epoch_time', 'random_number', 'cpu_usage']
sensors = ['epoch_time', 'random_number', 'cpu_usage', 'large_random_number']


hostname = socket.gethostname()

while True:
    time.sleep(0.05)
    epochtime = int(time.time())

    # Obtain Data
    cpu_usage = os.popen("ps -A -o %cpu | awk '{s+=$1} END {print s " + '"%"' + "}'").read().rstrip()[:-1]
    # print(cpu_usage)

    random_number = randrange(10)
    large_random_number = randrange(100)

    data_out = [random_number, cpu_usage]
    data_out = [random_number, cpu_usage, large_random_number]

    if hostname == 'Erics-Mac-mini':
        host_dir = '/Users/ericmartinez/Dropbox/Kinetix/Product/Inertia/Software'
    else:
        host_dir = '/home/moxa'

    # Store Data
    filelist = sorted(os.listdir(host_dir + '/data'))
    filelist.remove('archive')
    # print(filelist)
    try:
        latest_file = host_dir + '/data/' + str(filelist[-1])
    except:
        print('No Data File Found')
        latest_file = "empty.csv"
    data_filename = host_dir + '/data/' + str(epochtime) + '.csv'
    try:
        with open(latest_file) as f:
            latest_file_sensors = f.readline().rstrip().split(',')
    except:
        latest_file_sensors = []
    # print(latest_file_sensors)
    # print(latest_file[:-8], data_filename[:-8])
    if (latest_file[:-9] == data_filename[:-9]) and all(item in latest_file_sensors for item in sensors) and all(item in sensors for item in latest_file_sensors):
        data_filename = latest_file
    else:
        data_filename = latest_file
        data_filename = host_dir + '/data/' + str(epochtime) + '.csv'
        with open(data_filename, 'w') as f:
            for idx, sensor in enumerate(sensors):
                f.write(str(sensor))
                if idx != (len(sensors) - 1):
                    f.write(',')
            f.write('\n')
    with open(data_filename, 'a+') as f:
        f.write(str(epochtime) + ',')
        for idx, data_item in enumerate(data_out):
            f.write(str(data_item))
            if idx != (len(sensors) - 2):
                f.write(',')
        f.write('\n')
    # print(data_filename)



    sleeptime = 1.0 - (time.time() - int(time.time()))
    # print(epochtime, data_out, sleeptime, data_filename)
    time.sleep(sleeptime)