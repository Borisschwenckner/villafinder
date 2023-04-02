#SHELL=/bin/sh
#PATH=/usr/bin:/bin:/sbin:/usr/sbin


dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

./scrap_functions.py

./scrap_gorg.py


./get_web_frontend.sh
./sicher_scraper.sh
