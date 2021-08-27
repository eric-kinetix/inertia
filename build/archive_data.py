from datetime import datetime
import os
import socket
import subprocess

hostname = socket.gethostname()
if hostname == 'Erics-Mac-mini':
    host_dir = '/Users/ericmartinez/Dropbox/Kinetix/Product/Inertia/Software'
else:
    host_dir = '/home/moxa'

# Read files
filelist = sorted(os.listdir(host_dir + '/data'))
filelist.remove('archive')
try:
    filelist.remove('.DS_Store')
except:
    pass
print(filelist)
latest_file = filelist[-1]
print(latest_file)

testdt = datetime.utcnow()

# Loop through Files
for filename in filelist:
    # Send to archive
    print('Archiving', filename)
    os.system('rm -f ' + host_dir + '/data/archive/' + filename + '.zip')
    archive_script = 'zip ' + host_dir + '/data/archive/' + filename + '.zip ' + host_dir + '/data/' + filename
    print(archive_script)
    os.system(archive_script)

    # Remove file if in archive
    if (filename != latest_file) and (os.path.exists(host_dir + '/data/archive/' + filename + '.zip')):
        os.system('rm -f ' + host_dir + '/data/' + filename)
        print('Removed', filename)

# Send archived data to Volume
# send_to_volume_command = 'rsync -zuv /home/moxa/data/archive/* ' + hostname + '@volume.kinetix.energy:/home/' + hostname + '/data/archive'
# print(send_to_volume_command)
# os.system(send_to_volume_command)

