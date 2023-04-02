#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4 as bs
import urllib.request, os, time, sys
from datetime import date
today = date.today()
day = today.strftime("%d")
print(day)
sys.path.append('/prg/')
sys.path.append('../')
import functions
cur, conn = functions.connect_properties()

def fullscan():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'DC'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    print(site, sitemap_xml)
    sites = ''

    try:
        os.remove(sitemap_xml)
    except OSError as e: # name the Exception `e`
        print ("Failed with:", e.strerror) # look what it says

    links_for_db = []

    max = 500
    print(max)
    for seite in range(1,max): #
        print("Loop " + str(seite) + " startet.")
        try:
            links_found = 0
            new_links = 0
            try:
                soup = bs.BeautifulSoup(urllib.request.urlopen("https://dc-mallorca.com/de/immobilien/expose/page/" + str(seite) ).read(),'lxml')
            except:
                pass
            print("Aktuelle Seite FULLSCAN: "+"https://dc-mallorca.com/de/immobilien/expose/page/" + str(seite))

            for links in soup.find_all("a"):
                if r"/expose/" in str(links.get("href")) and  "page" not in str(links.get("href")) and  str(links.get("href"))[-2].isdigit()  :
                    links_found += 1
                    link =  (links.get("href").split("#")[0])
                    if link not in str(sites):
                        sites = sites + ('<url><loc>' + link + '</loc></url>\n')
                        links_for_db.append(link)
                        new_links += 1
            print (links_found, new_links)
            if new_links == 0 and seite > 10:
                print('keine neuen Links gefunden 2')
                g = open(sitemap_xml, "w")#
                g.write(sites)
                g.close
                for link_for_db in links_for_db:
                    cur.execute("INSERT INTO sitemap ( site, url) values ( %s, %s)" , ( [site ,link_for_db]))
                cur.execute("commit;")
                break
        except:
            pass




if __name__== "__main__":
      #if (day == '02' or day == '12' or  day == '22' ):
      fullscan()
      #only_new()
      print("FERTIG!")
