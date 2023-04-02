#!/usr/bin/python3
import bs4 as bs
import urllib.request, os, sys, re
from urllib.parse import urlparse
from datetime import datetime
from urllib.request import urlretrieve
import scrap_functions

dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
cur, conn = scrap_functions.connect_properties()


cur.execute("select id , name from cron where run_next_time =1 order by sort; ")
rows = cur.fetchall()
for row in rows:
    try:    
        id = row[0]
        name_func = ('scrap_functions.' + row[1] +'()'  )

        print (id)
        print (name_func)
        eval(name_func)
    except:
        pass
    cur.execute("update cron set run_next_time = 0 where id = %s;",([id]))
    cur.execute("commit;")


conn.close
