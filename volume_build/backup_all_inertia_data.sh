#!/bin/bash

cd /home/
for d in *; do
	echo $d
	mkdir -p /root/inertia/data/$d
	mkdir -p /root/inertia/data/$d/archive
	cp -r /home/$d/data/archive/*.zip /root/inertia/data/$d/archive/

done
