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
    @staticmethod
    def scrap():
        logger = com_logger.Logger('Scraper')
        url_start = "https://www.leboncoin.fr/annonces/offres/haute_normandie/occasions/?o="
        url_search = "&q="
        url_end = "&it=1"  # vide sinon recherche uniquement dans le titre "&it=1"
        search_list = []
        
        # Get Things to search from config file
        conf = com_config.Config()
        config = conf.getconfig()
        for i in range(1, 50):
            strthings = 'things' + str(i)
            try:
                if len(config['SEARCH'][strthings]) != 0:
                    search_list.append(config['SEARCH'][strthings])
            except Exception as exp:
                logger.error('File config error' + str(exp))
                break
        
        logger.info('Start extraction')
        
        for search_item in search_list:
            tab = search_item.split(",")
            prix_min = int(tab[1])
            prix_max = int(tab[2])
            index = 1
            contenuhtml = []
            
            logger.info('Search: ' + urllib.parse.unquote(tab[0]))
            
            urlok = 0
            try:
                urlok = requests.get(url_start + str(index) + url_search + urllib.parse.quote(tab[0]) + url_end).status_code
            except Exception as exp:
                logger.error('URL: ' + url_start + str(index) + url_search + urllib.parse.quote(tab[0]) + url_end)
                logger.error(str(exp))
            while urlok == 200:
                try:
                    url = urllib.request.urlopen(url_start + str(index) + url_search + urllib.parse.quote(tab[0]) + url_end).read()
                except Exception as exp:
                    logger.error('URL: ' + url_start + str(index) + url_search + urllib.parse.quote(tab[0]) + url_end)
                    logger.error(str(exp))
                    break
                
                soup = BeautifulSoup(url, "html.parser")
                soup.prettify()
                
                if len(soup.find_all("section", class_ = "tabsContent block-white dontSwitch")) == 0:
                    break
                
                for section in soup.find_all("section", class_ = "tabsContent block-white dontSwitch"):
                    for li in section.find_all("li"):
                        link = li.find("a", class_ = "list_item clearfix trackable")["href"]
                        idx = li.find("a", class_ = "list_item clearfix trackable")["data-info"].strip().split(",", 7)[2].split(":", 2)[1].replace('"', "").strip()
                        # container = source.find('div', attrs={'id':'dlbox'})
                        imglink = ''
                        try:
                            imglink = li.find("span", class_ = "lazyload")["data-imgsrc"]
                        except Exception as exp:
                            logger.debug('No image: ' + str(exp))
                            pass
                        
                        for item in li.find_all("section", class_ = "item_infos"):
                            titre = urllib.parse.unquote(item.find("h2", class_ = "item_title").text.strip().replace("\n", "").replace("\t", ""))
                            try:
                                prix = int(item.find("h3", class_ = "item_price").text.encode("ASCII", 'ignore').strip())
                            except AttributeError:
                                prix = 0
                            except ValueError:
                                prix = 0
                            
                            if (prix >= prix_min) and (prix <= prix_max):
                                if com_sqlite.select(idx) == 0:  # Item not yet present in database
                                    logger.debug('Find: ' + titre)
                                    com_sqlite.insert(idx)
                                    contenuhtml = Scraper.mailcontent(contenuhtml, imglink, item, link, prix, titre)
                index += 1
                logger.info('Page : ' + str(index))
            
            if len(contenuhtml) > 0:
                com_email.send_mail_gmail("LeBonCoin: " + urllib.parse.unquote(tab[0]) + "  Prix: " + str(prix_min) + "-" + str(prix_max), contenuhtml)
                logger.info('Mail sent')
        logger.info('End extraction')
    
    @staticmethod
    def mailcontent(contenuhtml, imglink, item, link, prix, titre):
        contenuhtml.append("<H2>" + str(titre) + "</H2>")
        for subitem in item.find_all("p", class_ = "item_supp"):
            contenuhtml.append(subitem.text.strip().replace("\n", "").replace(" ", ""))
        contenuhtml.append("<STRONG>" + str(prix) + " euro</STRONG>")
        if imglink:
            contenuhtml.append("<a href='" + str(link) + "'><img src='http:" + str(imglink) + "'></a>")
        contenuhtml.append("\n")
        return contenuhtml
