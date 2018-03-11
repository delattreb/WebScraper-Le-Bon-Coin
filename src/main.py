"""
Auteur: Bruno DELATTRE
Date : 01/09/2016
"""

import scraper
from lib import com_config

conf = com_config.Config()
# conf.setconfig()

scrap = scraper.Scraper()
scrap.scrap()
