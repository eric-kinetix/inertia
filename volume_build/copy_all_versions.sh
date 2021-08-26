#!/bin/bash

for d in /home/*; do
	echo $d
	mkdir -p $d/build
	cp -r /root/inertia/build/archive/*.zip $d/build/

done
