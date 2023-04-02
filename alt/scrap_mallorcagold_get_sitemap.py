#!/usr/bin/python3
# -*- coding: utf-8 -*-
import bs4 as bs
import urllib.request, os, time
from datetime import date
import requests
today = date.today()
day = today.strftime("%d")
print(day)

base_url ='https://mallorcagold.com/de/immobilien?tx_ntzproperties_properties%5Baction%5D=listarea&tx_ntzproperties_properties%5Bcontroller%5D=Properties&tx_ntzproperties_properties%5Bnumber_objects%5D=10&tx_ntzproperties_properties%5Bpage%5D='
base_url_suffix = '&cHash=c989185c31d0ea44b2d7f1873e12ed64'
#                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; WOW64; rv:40.0) Gecko/20100101 Firefox/40.0",


def fullscan():
    dirname = os.path.dirname(os.path.abspath(__file__)) + '/'
    site = 'Mallorcagold'
    sitemap_xml =   dirname + 'sitemap_' + site.lower() + '.xml'
    print(site, sitemap_xml)
    sites = ''
    max = 1000
    request_headers = {
                "Accept-Language": "en-US,en;q=0.5",
                "User-Agent": "Mozilla/5.0 (compatible; Googlebot/2.1; +http://www.google.com/bot.html)",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Referer": "https://google.com",
                "Connection": "keep-alive"}
    for seite in range(0,max): #
        print("Loop " + str(seite) + " startet.")
        try:
            #if 1 > 0:
              #print (seite)
                links_found = 0
                new_links = 0
                headers = request_headers
                page = requests.get(base_url +str(seite) + base_url_suffix)
                soup = bs.BeautifulSoup(page.content,'lxml')
                print("Aktuelle Seite FULLSCAN: "+base_url+ str(seite)+base_url_suffix)
                for links in soup.find_all("a"):
                    if r"/expose/" in str(links.get("href")) and 'twitter' not in str(links.get("href")) and 'facebook' not in str(links.get("href")) and 'whatsapp' not in str(links.get("href")) and 'print' not in str(links.get("href"))  :
                        link =  ('https://mallorcagold.com' + links.get("href").split("#")[0])
                        links_found += 1
                        if link not in str(sites):
                            new_links += 1
                            sites = sites + ('<url><loc>' + link + '</loc></url>\n')
                print (links_found, new_links)
                if new_links == 0 and seite > 10:
                    print('Keine neuen Links gefunden')
                    print (sites.count('<url><loc>'))
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
