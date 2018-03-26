"""
Auteur: Bruno DELATTRE
Date : 07/08/2016
"""

import sqlite3

from lib import com_config


def connect():
    conf = com_config.Config()
    config = conf.getconfig()
    con = sqlite3.connect(config['SQLITE']['database'])
    cursor = con.cursor()
    return con, cursor

# Le bon coin
def select(val):
    con, cursor = connect()
    rows = cursor.execute("SELECT id FROM data WHERE id='" + str(val) + "'")
    id = 0
    for row in rows:
        id = row[0]
    con.close()
    return id


def insert(val):
    con, cursor = connect()
    try:
        cursor.execute("INSERT INTO data(id) VALUES('" + str(val) + "')")
        con.commit()
    except:
        con.rollback()
    con.close()


def delete(val):
    con, cursor = connect()
    try:
        cursor.execute("DELETE FROM data WHERE id ='" + str(val) + "'")
        con.commit()
    except:
        con.rollback()
    con.close()

# Okkazeo
def selectokkazeo(title, datepar):
    con, cursor = connect()
    rows = cursor.execute("SELECT title FROM okkazeo WHERE datepar='" + str(datepar) + "' AND title='"+ str(title)+"'")
    title = 0
    for row in rows:
        title = row[0]
    con.close()
    return title


def insertokkazeo(title, datepar):
    con, cursor = connect()
    try:
        cursor.execute("INSERT INTO okkazeo(title, datepar) VALUES('" + title + "','"+ datepar + "')")
        con.commit()
    except:
        con.rollback()
    con.close()
