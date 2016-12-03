"""
Auteur: Bruno DELATTRE
Date : 01/09/2016
"""

import scraper
from lib import com_config

com_config.setConfig ()
scrap = scraper.Scraper ()
scrap.scrap ()
