"""
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import configparser
import os.path

config_file = "config/config.ini"


def setConfig():
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
    config['SEARCH']['things1'] = 'maquette 1/35,10,25'
    config['SEARCH']['things2'] = 'pentax boitier,30,300'
    config['SEARCH']['things3'] = 'mini serre plante,5,30'
    
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, config_file)
    with open(db_path, 'w') as configfile:
        config.write(configfile)


def getConfig():
    config = configparser.RawConfigParser()
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))
    db_path = os.path.join(BASE_DIR, config_file)
    config.read(db_path)
    return config
