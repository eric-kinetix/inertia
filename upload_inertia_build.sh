#!/bin/bash
VERSION="I_0_0_2"

echo $VERSION > build/version.txt
zip $VERSION.zip -r build/.
mv $VERSION.zip archive
#scp -r build/ moxa@192.168.2.77:/home/moxa/build/$VERSION/
scp archive/$VERSION.zip root@volume.kinetix.energy:/root/inertia/build/archive

ssh root@volume.kinetix.energy 'bash /root/inertia/build/volume_build/copy_all_versions.sh'