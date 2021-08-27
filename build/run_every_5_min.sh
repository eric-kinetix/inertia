#!/bin/bash

/usr/bin/python3 /home/moxa/build/current/archive_data.py
sshpass -p $HOSTNAME /usr/bin/rsync -zuv /home/moxa/data/archive/* $HOSTNAME@volume.kinetix.energy:/home/$HOSTNAME/data/archive >> /tmp/rsync_out_log
