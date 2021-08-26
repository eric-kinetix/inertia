#!/bin/bash

/usr/bin/python3 /home/moxa/build/current/archive_data.py
sshpass -p $HOSTNAME /usr/bin/rsync -zuv /home/moxa/data/archive/* $HOSTNAME@50.116.12.234:/home/$HOSTNAME/data/archive >> /tmp/rsync_out_log
