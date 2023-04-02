#SHELL=/bin/sh
#PATH=/usr/bin:/bin:/sbin:/usr/sbin


dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

path="/mnt/video/netz"

pg_dump "host=sql12.your-server.de sslrootcert=/prg/keys/psqlca.pem sslmode=verify-ca user=schweng_2  password='v9gyQ62fetFM2jDU' dbname=properies" -f ./db_backup/properties-latest.dmp
tar -cvzf $path/sicher/sonstiges/scraper-latest.tar.gz $path/prg/scraper

set sftp:auto-confirm yes
HOST="u166165.your-storagebox.de"
USER="u166165"

##sudo lftp -u ${USER},${PASS} sftp://${HOST}:422 <<EOF
sudo lftp -u ${USER}, sftp://${HOST} <<EOF
mkdir /ftp/scraper/
mkdir /ftp/scraper/db_backup
mkdir /ftp/scraper/stable

cd /ftp/scraper/
mput -e $dir/*

cd /ftp/scraper/db_backup/
mput -e $dir/db_backup/*

put $path/sicher/sonstiges/scraper-latest.tar.gz


bye
EOF
#huhu

#cp $path/sicher/sonstiges/scraper-latest.tar.gz /mnt/hetzner/ftp/scraper/scraper-latest.tar.gz
#cp $dir/* /mnt/hetzner/ftp/scraper/
#echo $dir
