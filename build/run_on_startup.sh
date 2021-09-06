#!/bin/bash

/usr/bin/python3 /home/moxa/build/current/data_collection.py &
/usr/bin/python3 /home/moxa/build/current/send_current_data_to_memory.py &