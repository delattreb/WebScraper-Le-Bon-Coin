"""
com_logger.py v1.1.0
Auteur: Bruno DELATTRE
Date : 14/08/2016
"""

import logging
import colorlog

from lib import com_config
from logging.handlers import RotatingFileHandler


class Logger:
    def __init__(self, name='', file=''):
        self.config = com_config.getConfig()
        self.logger = logging.Logger(name, logging.DEBUG)
        self.logger.name = name
        
        # Formatter
        formatterfile = logging.Formatter('%(asctime)s %(levelname)s : %(name)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S')
        formatterconsole = colorlog.ColoredFormatter('%(asctime)s %(log_color)s%(levelname)s : %(name)s - %(message)s', datefmt='%d/%m/%Y %H:%M:%S',
                                                     log_colors={'DEBUG':    'white', 'INFO': 'green',
                                                                 'WARNING':  'bold_yellow', 'ERROR': 'bold_red',
                                                                 'CRITICAL': 'bold_red'})
        
        # First logger (file)
        self.logger.setLevel(logging.DEBUG)
        file_handler = RotatingFileHandler(self.config['LOGGER']['logfile'], 'a', int(self.config['LOGGER']['logfilesize']), 1)
        file_handler.setLevel(int(self.config['LOGGER']['levelfile']))
        file_handler.setFormatter(formatterfile)
        self.logger.addHandler(file_handler)
        
        # second logger (console)
        steam_handler = logging.StreamHandler()
        steam_handler.setLevel(int(self.config['LOGGER']['levelconsole']))
        steam_handler.setFormatter(formatterconsole)
        self.logger.addHandler(steam_handler)
    
    def info(self, strinfo):
        self.logger.info(strinfo)
    
    def debug(self, strdebug):
        self.logger.debug(strdebug)
    
    def warning(self, strwarning):
        self.logger.warning(strwarning)
    
    def error(self, strerror):
        self.logger.error(strerror)
    
    def critical(self, strcritical):
        self.logger.critical(strcritical)
