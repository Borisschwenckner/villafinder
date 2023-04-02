#SHELL=/bin/sh
PATH=/usr/bin:/bin:/sbin:/usr/sbin

path="/mnt/video/netz/prg/scraper/" #/mnt/video/netz/prg/scraper


dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

set sftp:auto-confirm yes
HOST="u166165.your-storagebox.de"
USER="u166165"

#sudo lftp -u ${USER},${PASS} sftp://${HOST}:422 <<EOF
sudo lftp -u ${USER}, sftp://${HOST} <<EOF
cd /ftp/scraper/
mget -e *

#cd /ftp/scraper/stable/
#mget -e *

bye
EOF
