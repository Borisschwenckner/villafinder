#SHELL=/bin/sh
#PATH=/usr/bin:/bin:/sbin:/usr/sbin


dir=$(dirname $(readlink -f $0))
echo $dir
cd $dir

./scrap_functions.py

./scrap_gorg.py

./sicher_scraper.sh
