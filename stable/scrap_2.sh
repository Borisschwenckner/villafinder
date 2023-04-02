#SHELL=/bin/sh
#PATH=/usr/bin:/bin:/sbin:/usr/sbin


dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

sudo chmod -R 777 $dir
./get_scraper.sh
sudo chmod -R 777 $dir


./scrap_functions.py
