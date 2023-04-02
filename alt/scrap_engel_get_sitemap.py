#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4 as bs
import requests
import urllib.request, os, time
from datetime import date
today = date.today()
day = today.strftime("%d")
print(day)


base_url ='https://www.engelvoelkers.com/de/search/?q=&startIndex='
base_url_suffix = '&businessArea=residential&sortOrder=DESC&sortField=sortPrice&pageSize=18&facets=bsnssr%3Aresidential%3Bcntry%3Aspain%3Brgn%3Amajorca%3Btyp%3Abuy%3B'
objects_per_page = 18

def fullscan():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'Engel'
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
        if seite ==1 :
            index = 1
        else:
            index = seite * objects_per_page
        print(index)

        try:
        #if 1>0:
            page = requests.get(base_url +str(index) + base_url_suffix)
            soup = bs.BeautifulSoup(page.content,'lxml')
            print("Aktuelle Seite FULLSCAN: "+base_url+ str(index)+base_url_suffix)
            for links in soup.find_all("a"):
                #print(str(links.get("href")))
                if r"/exposes" in str(links.get("href"))  :
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
