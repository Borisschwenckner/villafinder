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
    site = 'Casanova'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    print(site, sitemap_xml)
    sites = ''

    try:
        os.remove(sitemap_xml)
    except OSError as e: # name the Exception `e`
        print ("Failed with:", e.strerror) # look what it says
        #print ("Error code:", e.code)
    if os.path.exists(sitemap_xml):
        print ('NOT Deleted: ', sitemap_xml)
    else:
        print ('Deleted: ', sitemap_xml)


    max = 1000

    for seite in range(1,max): #
        print("Loop " + str(seite) + " startet.")
        links_found = 0
        new_links = 0
        try:
            soup = bs.BeautifulSoup(urllib.request.urlopen("https://www.casanova-immobilienmallorca.de/de/immobilien-mallorca/" + str(seite) ).read(),'lxml')
            print("Aktuelle Seite FULLSCAN: "+"https://www.casanova-immobilienmallorca.de/de/immobilien-mallorca/" + str(seite))
            for links in soup.find_all("a"):
                if r"/expose" in str(links.get("href"))  :
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
