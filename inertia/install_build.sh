#!/bin/bash

scp -r $HOSTNAME@volume.kinetix.energy:/home/$HOSTNAME/build/*.zip /home/moxa/build/archive/

mkdir /home/moxa/build/temp
unzip /home/moxa/build/archive/$1.zip -d /home/moxa/build/temp/
cp -a /home/moxa/build/temp/build/. /home/moxa/build/current/
echo "Copied: $1"
rm -r /home/moxa/build/temp
chmod +x /home/moxa/build/current/run_on_install.sh
chmod +x /home/moxa/build/current/run_on_startup.sh
bash /home/moxa/build/current/run_on_install.sh
