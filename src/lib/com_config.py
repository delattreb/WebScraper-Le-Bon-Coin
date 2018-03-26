"""
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


class Config:
    def __init__(self):
        self.config = configparser.ConfigParser()
    
    def setconfig(self):
        # EMAIL
        self.config['EMAIL'] = {}
        self.config['EMAIL']['from'] = 'pythonuseriot@gmail.com'
        self.config['EMAIL']['to'] = 'delattreb@gmail.com'
        self.config['EMAIL']['password'] = 'pythonuser'
        
        # LOGGER
        self.config['LOGGER'] = {}
        self.config['LOGGER']['levelconsole'] = '10'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
        self.config['LOGGER']['levelfile'] = '20'
        self.config['LOGGER']['logfile'] = 'log'
        self.config['LOGGER']['logfilesize'] = '1000000'
        self.config['LOGGER']['lognumber'] = '2'

        # SQLite
        self.config['SQLITE'] = {}
        self.config['SQLITE']['database'] = 'database.db'
        
        # Search Le Bon Coin
        self.config['SEARCHLBC'] = {}
        self.config['SEARCHLBC']['max_browse'] = '10'
        self.config['SEARCHLBC']['things1'] = 'vtt,150,300'
        self.config['SEARCHLBC']['things2'] = 'raspberry,10,30'
        self.config['SEARCHLBC']['things3'] = 'vieille radio,5,40'
        self.config['SEARCHLBC']['things4'] = 'cerf volant,40,250'

        # Search Okkazeo
        self.config['SEARCHOKKAZEO'] = {}
        self.config['SEARCHOKKAZEO']['max_browse'] = '10'
        self.config['SEARCHOKKAZEO']['things1'] = 'Yokohama,10,100'
        self.config['SEARCHOKKAZEO']['things2'] = 'fortune,10,30'


        basedir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(basedir, config_file)
        with open(db_path, 'w') as configfile:
            self.config.write(configfile)
    
    def getconfig(self):
        self.config = configparser.RawConfigParser()
        base_dir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(base_dir, config_file)
        self.config.read(db_path)
        return self.config
