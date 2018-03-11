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
        url_start = "https://www.leboncoin.fr/annonces/offres/haute_normandie/?o="
        #https://www.leboncoin.fr/annonces/offres/?th=1
        #https: // www.leboncoin.fr/annonces/offres/haute_normandie/?th = 1 & q = vtt
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
                #logger.error('File config error' + str(exp))
                break

        logger.info('Start extraction')

        for search_item in search_list:
            tab = search_item.split(",")
            prix_min = int(tab[1])
            prix_max = int(tab[2])
            index = 1
            contenuhtml = []
            contenu = []

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
                            titre = urllib.parse.unquote(item.find("h2", class_ = "item_title").text.replace("\n", "").replace("\t", ""))
                            category = urllib.parse.unquote(item.find("p", itemprop = "category").text.replace("\n", "").replace("\t", ""))
                            localisation = urllib.parse.unquote(item.find("p", itemprop = "availableAtOrFrom").text.replace("\n", "").replace("\t", ""))

                            try:
                                prix = int(item.find("h3", class_ = "item_price").text.encode("ASCII", 'ignore').strip())
                            except AttributeError:
                                prix = 0
                            except ValueError:
                                prix = 0

                            if (prix >= prix_min) and (prix <= prix_max):
                                if com_sqlite.select(idx) == 0:  # Item not yet present in database
                                    logger.info('Find: ' + titre.strip())
                                    com_sqlite.insert(idx)
                                    contenuhtml = Scraper.mailContent(contenuhtml, imglink, link, prix, titre, category, localisation)
                index += 1
                logger.debug('Page : ' + str(index))

            if len(contenuhtml) > 0:
                contenu = Scraper.mailFull("LeBonCoin: " + urllib.parse.unquote(tab[0]) + "  Prix: " + str(prix_min) + "-" + str(prix_max)+' €', contenuhtml)
                com_email.send_mail_gmail("LeBonCoin: " + urllib.parse.unquote(tab[0]) + "  Prix: " + str(prix_min) + "-" + str(prix_max)+' €', contenu)
                logger.info('Mail sent')
        logger.info('End extraction')

    @staticmethod
    def mailContent(contenuhtml, imglink, link, prix, titre, category, localisation):
        contenuhtml.append('<tr><td colspan="3"><h2 style="color:#0E7693; font-size:22px; padding-top:12px;">' + str(titre) +' - '+str(prix)+' €'+'</h2></td></tr>')
        contenuhtml.append('<tr><td class="w275" width="275" valign="top"><div align="left" class="article-content"><p></p>')
        contenuhtml.append('<ul>')
        contenuhtml.append('<li>' + str(category) + '</li>')
        contenuhtml.append('<li>' + str(localisation) + '</li>')
        contenuhtml.append('</ul></div></td><td class="w30" width="30" class="w30"></td><td class="w275" width="275" valign="top"><div align="left" class="article-content"><p>')
        if imglink:
            contenuhtml.append("<a href='" + str(link) + "'><img src='" + str(imglink) + "'></a>")
        contenuhtml.append('</p></div></td></tr>')

        return contenuhtml

    @staticmethod
    def mailFull(titre, contenuhtml):
        contenu = []

        # entete
        contenu.append('<!DOCTYPE HTML PUBLIC "-//W3C//DTD XHTML 1.0 Transitional //EN" "http://www.w3.org/TR/xhtml1/DTD/xhtml1-transitional.dtd"><html xmlns="http://www.w3.org/1999/xhtml"><head><title>Le bon coin</title><meta http-equiv="Content-Type" content="text/html; charset=utf-8"><meta content="width=device-width"><style type="text/css">body, td {font-family: "Helvetica Neue", Arial, Helvetica, Geneva, sans-serif;font-size: 14px;}body {background-color: #2A374E;margin: 0;padding: 0;-webkit-text-size-adjust: none;-ms-text-size-adjust: none;}h2 {padding-top: 12px;color: #0E7693;font-size: 22px;}@media only screen and (max-width: 480px) {table[class=w275], td[class=w275], img[class=w275] {width: 135px !important;}table[class=w30], td[class=w30], img[class=w30] {width: 10px !important;}table[class=w580], td[class=w580], img[class=w580] {width: 280px !important;}table[class=w640], td[class=w640], img[class=w640] {width: 300px !important;}img {height: auto;}table[class=w180], td[class=w180], img[class=w180] {width: 280px !important;display: block;}td[class=w20] {display: none;}}</style></head><body style="margin:0px; padding:0px; -webkit-text-size-adjust:none;"><table width="100%" cellpadding="0" cellspacing="0" border="0" style="background-color:rgb(42, 55, 78)"><tbody><tr><td align="center" bgcolor="#2A374E"><table cellpadding="0" cellspacing="0" border="0"><tbody><tr><td class="w640" width="640" height="10"></td></tr><tr></tr><tr><td class="w640" width="640" height="10"></td></tr><tr class="pagetoplogo"><td class="w640" width="640"><table class="w640" width="640" cellpadding="0" cellspacing="0" border="0" bgcolor="#F2F0F0"><tbody><tr><td class="w30" width="30"></td><td class="w580" width="580" valign="middle" align="left"><div class="pagetoplogo-content"><h2 style="color:#0E7693; font-size:26px; padding-top:12px;">'+str(titre)+'</h2></div></td><td class="w30" width="30"></td></tr></tbody></table></td></tr><tr><td class="w640" width="640" height="1" bgcolor="#d7d6d6"></td></tr><tr class="content"><td class="w640" class="w640" width="640" bgcolor="#ffffff"><table class="w640" width="640" cellpadding="0" cellspacing="0" border="0"><tbody><tr><td class="w30" width="30"></td><td class="w580" width="580"><table class="w580" width="580" cellspacing="0" cellpadding="0" border="0"><tbody>')

        contenu.append(contenuhtml)

        # pied
        contenu.append('<tr><td colspan="3" class="w580" height="1" bgcolor="#c7c5c5"></td></tr></tbody></table></td><td class="w30" class="w30" width="30"></td></tr></tbody></table></td></tr><tr><td class="w640" width="640" height="15" bgcolor="#ffffff"></td></tr><tr class="pagebottom"><td class="w640" width="640"><table class="w640" width="640" cellpadding="0" cellspacing="0" border="0" bgcolor="#c7c7c7"><tbody><tr><td colspan="5" height="10"></td></tr><tr><td class="w30" width="30"></td><td class="w580" width="580" valign="top"><p align="right" class="pagebottom-content-left"><a style="color:#255D5C;" href=""><span style="color:#255D5C;"></span></a></p></td><td class="w30" width="30"></td></tr><tr><td colspan="5" height="10"></td></tr></tbody></table></td></tr><tr><td class="w640" width="640" height="60"></td></tr></tbody></table></td></tr></tbody></table></body></html>')
        return contenu
