"""
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


class Config:
    def setconfig(self):
        config = configparser.ConfigParser()
        
        # EMAIL
        config['EMAIL'] = {}
        config['EMAIL']['from'] = 'pythonuseriot@gmail.com'
        config['EMAIL']['to'] = 'delattreb@gmail.com'
        config['EMAIL']['password'] = 'pythonuser'
        
        # LOGGER
        config['LOGGER'] = {}
        config['LOGGER']['levelconsole'] = '10'  # DEBUG=10 INFO=20 WARNING=30 ERROR=40 #CRITICAL=50
        config['LOGGER']['levelfile'] = '20'
        config['LOGGER']['logfile'] = 'log'
        config['LOGGER']['logfilesize'] = '1000000'
        
        # SQLite
        config['SQLITE'] = {}
        config['SQLITE']['database'] = 'database.db'
        
        # Search
        config['SEARCH'] = {}
        config['SEARCH']['things1'] = 'maquette tamiya 1/35,1,30'
        config['SEARCH']['things2'] = 'raspberry,10,30'
        config['SEARCH']['things3'] = 'vieille radio,5,40'
        config['SEARCH']['things4'] = 'cerf volant,40,250'
        
        basedir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(basedir, config_file)
        with open(db_path, 'w') as configfile:
            config.write(configfile)
    
    def getconfig(self):
        config = configparser.RawConfigParser()
        basedir = os.path.dirname(os.path.abspath(__file__))
        db_path = os.path.join(basedir, config_file)
        config.read(db_path)
        return config
