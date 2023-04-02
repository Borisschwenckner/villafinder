#SHELL=/bin/sh
PATH=/usr/bin:/bin:/sbin:/usr/sbin

path="/mnt/video/netz/prg/scraper/" #/mnt/video/netz/prg/scraper
# Wenn kein Connectmöglich ist:
#sftp schweng@schwenckner.net -p222

dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

cd web_frontend

set sftp:auto-confirm yes
HOST="schwenckner.net"
USER="schweng_11"
PASS="SF2wt5CL93dB39BV"

lftp  -u ${USER},${PASS} sftp://${HOST}:22 <<EOF
#sudo lftp -u ${USER}, sftp://${HOST}:22 <<EOF
#cd /
#mget -v -e *
mirror --continue --exclude images/

#put gorg.csv

#cd /ftp/scraper/stable/
#mget -e *

bye
EOF
