#SHELL=/bin/sh
PATH=/usr/bin:/bin:/sbin:/usr/sbin

path="/mnt/video/netz/prg/scraper/" #/mnt/video/netz/prg/scraper


dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

#cd web_frontend

set sftp:auto-confirm yes
HOST="www28.your-server.de"
USER="schweng_10"
PASS="Zcr76b6wG712tcKg"

lftp -u ${USER},${PASS} sftp://${HOST}:22 <<EOF
#sudo lftp -u ${USER}, sftp://${HOST}:22 <<EOF
#cd /
#mget -e *
put gorg.csv

#cd /ftp/scraper/stable/
#mget -e *

bye
EOF
