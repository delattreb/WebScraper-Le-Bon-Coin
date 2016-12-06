"""
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import urllib.parse
import urllib.request

import requests
from bs4 import BeautifulSoup

from lib import com_config, com_email, com_logger, com_sqlite


class Scraper:
    def scrap(self):
        logger = com_logger.Logger('Scraper')
        url_start = "https://www.leboncoin.fr/annonces/offres/haute_normandie/occasions/?o="
        url_search = "&q="
        url_end = ""  # sinon recherche uniquement dans le titre  "&it=1"
        search_list = []
        
        # Get Things to search from config file
        config = com_config.getConfig()
        for i in range(1, 50):
            strThings = 'things' + str(i)
            try:
                if len(config['SEARCH'][strThings]) != 0:
                    search_list.append(config['SEARCH'][strThings])
            except:
                break
        
        logger.info('Start extraction')
        
        for search_item in search_list:
            tab = search_item.split(",")
            prix_min = int(tab[1])
            prix_max = int(tab[2])
            index = 1
            contenuHTML = []
            
            logger.info('Search: ' + urllib.parse.unquote(tab[0]))
            
            while requests.get(url_start + str(index) + url_search + urllib.parse.quote(tab[0]) + url_end).status_code == 200:
                url = urllib.request.urlopen(url_start + str(index) + url_search + urllib.parse.quote(tab[0]) + url_end).read()
                soup = BeautifulSoup(url, "html.parser")
                soup.prettify()
                
                if len(soup.find_all("section", class_ = "tabsContent block-white dontSwitch")) == 0:
                    break
                
                for section in soup.find_all("section", class_ = "tabsContent block-white dontSwitch"):
                    for li in section.find_all("li"):
                        link = li.find("a", class_ = "list_item clearfix trackable")["href"]
                        id = li.find("a", class_ = "list_item clearfix trackable")["data-info"].strip().split(",", 7)[2].split(":", 2)[1].replace('"', "").strip()
                        # container = source.find('div', attrs={'id':'dlbox'})
                        try:
                            imglink = li.find("span", class_ = "lazyload")["data-imgsrc"]
                        except:
                            pass
                        
                        for item in li.find_all("section", class_ = "item_infos"):
                            titre = urllib.parse.unquote(item.find("h2", class_ = "item_title").text.strip().replace("\n", "").replace("\t", ""))
                            try:
                                prix = int(item.find("h3", class_ = "item_price").text.encode("ASCII", 'ignore').strip())
                            except AttributeError:
                                prix = 0
                            except ValueError:
                                prix = 0
                            
                            if ((prix >= prix_min) and (prix <= prix_max)):
                                if com_sqlite.select(id) == 0:
                                    
                                    logger.debug('Find: ' + titre)
                                    
                                    com_sqlite.insert(id)
                                    contenuHTML.append("<H2>" + str(titre) + "</H2>")
                                    for subitem in item.find_all("p", class_ = "item_supp"):
                                        contenuHTML.append(subitem.text.strip().replace("\n", "").replace(" ", ""))
                                    contenuHTML.append("<STRONG>" + str(prix) + " euro</STRONG>")
                                    contenuHTML.append("<a href='" + str(link) + "'><img src='http:" + str(imglink) + "'></a>")
                                    contenuHTML.append("\n")
                index = index + 1
                logger.info('Page : ' + str(index))
            
            if len(contenuHTML) > 0:
                com_email.send_mail_gmail("LeBonCoin: " + urllib.parse.unquote(tab[0]) + "  Prix: " + str(prix_min) + "-" + str(prix_max), contenuHTML)
                logger.info('Mail sent')
        logger.info('End extraction')
