"""
Auteur: Bruno DELATTRE
Date : 01/09/2016
"""

import ScraperLeBonCoin, ScraperOkkazeo
from lib import com_config

conf = com_config.Config()
conf.setconfig()

#scraplbc = ScraperLeBonCoin.Scraper()
#scraplbc.scrap()

scrapokkazeo = ScraperOkkazeo.Scraper()
scrapokkazeo.scrap()