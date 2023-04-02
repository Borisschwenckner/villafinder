#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4 as bs
import urllib.request, os, time
from datetime import date
today = date.today()
day = today.strftime("%d")
print(day)




def fullscan():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'Remus'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    print(site, sitemap_xml)
    sites = ''


    try:
        os.remove(sitemap_xml)
    except OSError as e: # name the Exception `e`
        print ("Failed with:", e.strerror) # look what it says

    sites = ''
    max = 1000
    urls = ["https://www.marcelremusrealestate.com/immobilien/pg/"]
    for url in urls:
        for seite in range(1,max): #
            links_found = 0
            new_links = 0
            print("Loop " + str(seite) + " startet.")
            try:
            #if 1 > 0:
                soup = bs.BeautifulSoup(urllib.request.urlopen(url + str(seite)  ).read(),'lxml')
                print("Aktuelle Seite FULLSCAN: "+ url + str(seite))
                for links in soup.find_all("a"):
                    #print (str(links.get("href")))
                    if  r"/immobilien/" in str(links.get("href"))  :
                        if (links.get("href"))[-4].isdigit():
                            link =  (links.get("href").split("#")[0])
                            links_found += 1
                            if link not in str(sites):
                                new_links += 1
                                sites = sites + ('<url><loc>' + link + '</loc></url>\n')
                print (links_found, new_links)
                if new_links == 0 and seite > 10:
                    print('keine neuen Links gefunden 2')
                    g = open(sitemap_xml, "w")#
                    g.write(sites)
                    g.close
                    break


            except:
                pass




if __name__== "__main__":
      #if (day == '02' or day == '12' or  day == '22' ):
      fullscan()
      #only_new()
      print("FERTIG!")
