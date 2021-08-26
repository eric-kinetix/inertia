import requests, json
import time
from datetime import datetime
import os
import pandas as pd
import socket

from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
from influxdb import DataFrameClient

# You can generate a Token from the "Tokens Tab" in the UI
token = "7VKr4vYlsmXd5er9xDbe0GpvKlZBLUB9cQggvFInggHq-LJvFw7eDeq_CsrLr97uAryUvkeUQE-SlWiOto69kQ=="
org = "emartinez505@gmail.com"
bucket = "Inertia"

def get_timestamp_of_last_entry(inertia_idx):
    hour_idx = 1
    latest_time_found = False
    while ((hour_idx < 1000) and (latest_time_found == False)):
        try:
            query = 'from(bucket: "Inertia")\
            |> range(start:-' + str(hour_idx) + 'h, stop: now())\
            |> pivot(rowKey:["_time"], columnKey: ["_field"], valueColumn: "_value")\
            |> filter(fn: (r) => r.cpu == "' + inertia_idx + '")'

            # |> filter(fn: (r) => r._field == "temp")

            # client = InfluxDBClient(url="http://localhost:9999", token=token, org=org, debug=False)
            client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token, org=org)
            system_stats = client.query_api().query_data_frame(org=org, query=query)
            system_stats = system_stats.rename(columns={"_time": 'time'})
            system_stats.index = system_stats['time']
            system_stats = system_stats.drop(columns=['result', 'table', 'time', '_start', '_stop', '_measurement'])

            # system_stats.index.names = ['time']
            # print(system_stats.columns)
            # print(system_stats)

            latest_time = str(pd.to_datetime(system_stats.index.values[-1]).value)[:-9]

            print('latest time', latest_time)

            latest_time_found = True

            hour_idx += 1
        except:
            print('hour_idx', hour_idx)
            hour_idx += 1

    return latest_time

# Create Backups
os.system('bash /root/inertia/build/volume_build/backup_all_inertia_data.sh')

hostname = socket.gethostname()
# print('hostname', hostname)

client = InfluxDBClient(url="https://us-west-2-1.aws.cloud2.influxdata.com", token=token)
write_api = client.write_api(write_options=SYNCHRONOUS)

# Get each inertia
inertia_list = os.listdir('/root/inertia/data')
# print(inertia_list)
inertia_idx = 'inertia0'

# Read files
filelist = sorted(os.listdir('/root/inertia/data/' + inertia_idx + '/archive'))
# filelist.remove('archive')
# try:
#     filelist.remove('.DS_Store')
# except:
#     pass
# print(filelist)
latest_file = filelist[-1]
# print(latest_file)

testdt = datetime.utcnow()

os.system('mkdir -p /root/inertia/data/' + inertia_idx + '/archive/temp')

latest_time = get_timestamp_of_last_entry(inertia_idx)
latest_time_dt = pd.to_datetime(int(latest_time), unit='s')
latest_time_compare = int(latest_time[:5])

print(latest_time)
print(latest_time_dt)

# quit()

# Loop through Files
for filename in filelist:
    if filename[0] is not '1':
        continue

    if int(filename[:5]) < latest_time_compare:
        # print('skipped', int(filename[:5]), latest_time_compare)
        continue

    # print(int(filename[:5]), latest_time_compare)

    # quit()

    # Unzip to temp folder and get data
    os.system('unzip -o /root/inertia/data/' + inertia_idx + '/archive/' + filename + ' -d /root/inertia/data/' + inertia_idx + '/archive/temp')

    filename_no_zip = filename[:-4]
    # print(filename_no_zip)

    # Send data to influxdb
    data_df_filename = '/root/inertia/data/' + inertia_idx + '/archive/temp/home/moxa/data/' + filename_no_zip
    try:
        data_df = pd.read_csv(data_df_filename, index_col=0)
    except:
        print('could not extract', filename)
        continue
    data_df.index = pd.to_datetime(data_df.index, unit='s')
    # print(data_df)
    # quit()
    # print(data_df)
    new_data_df = data_df[data_df.index > latest_time_dt]
    # print(new_data_df)

    if not new_data_df.empty:
        new_data_df['cpu'] = inertia_idx
        write_api.write(bucket, org, record=new_data_df, data_frame_measurement_name=inertia_idx, data_frame_tag_columns=['cpu'], debug=True)

    #
    # # Remove file if in db
    # if (filename != latest_file) and (os.path.exists('data/archive/' + filename + '.zip')):
    #     print('Removed', filename)
    #     archive_out = os.popen('rm data/' + filename)
    # quit()

os.system('rm -r /root/inertia/data/' + inertia_idx + '/archive/temp')