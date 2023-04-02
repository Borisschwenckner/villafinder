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


def fullscan(site):

    cur.execute("select count(id)  from sitemap  where create_date = create_date and site = '" + site + "' " )
    qty = cur.fetchone()
    print('qty', qty[0])
    if qty[0] == 0:
        cur.execute("delete from sitemap  where site = '" + site + "' ")
        cur.execute("commit;")

        dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
        #site = 'DC-Mallorca'
        sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
        print(site, sitemap_xml)
        sites = ''

        cur.execute("select * from sites  where site = '" + site + "' ")
        result = cur.fetchone()
        sitemap_url = result[3]
        sitemap_url_suffix = result[4]
        #sitemap_selector = result[5]
        sitemap_selector ="""r"/expose/" in str(links.get("href")) and  "page" not in str(links.get("href")) and  str(links.get("href"))[-2].isdigit() """
        print(sitemap_url)

        try:
            os.remove(sitemap_xml)
        except OSError as e: # name the Exception `e`
            print ("Failed with:", e.strerror) # look what it says

        links_for_db = []

        #print(selectors)
        max =  500
        print(max)
        for seite in range(1,max): #
            print("Loop " + str(seite) + " startet.")
            #try:
            if 1 >0:
                links_found = 0
                new_links = 0
                try:
                    soup = bs.BeautifulSoup(urllib.request.urlopen(sitemap_url + str(seite) ).read(),'lxml')
                except:
                    pass
                print("Aktuelle Seite FULLSCAN: "+sitemap_url + str(seite))

                for links in soup.find_all("a" ):
                    if eval(sitemap_selector):
                        links_found += 1
                        #link =  (links.get("href").split("#")[0])
                        link =  (links.get("href"))
                        if link != None and  link not in str(sites) :
                            sites = sites + ('<url><loc>' + link + '</loc></url>\n')
                            links_for_db.append(link)
                            new_links += 1
                print (links_found, new_links)
                if new_links == 0 and seite > 10 : #10
                    print('keine neuen Links gefunden 2')
                    g = open(sitemap_xml, "w")#
                    g.write(sites)
                    g.close
                    for link_for_db in links_for_db:
                        cur.execute("INSERT INTO sitemap ( site, url) values ( %s, %s)" , ( [site ,link_for_db]))
                    cur.execute("commit;")
                    break
            #except:
            #    pass




if __name__== "__main__":
      #if (day == '02' or day == '12' or  day == '22' ):
      fullscan()
      #only_new()
      print("FERTIG!")
