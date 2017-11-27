#!/usr/bin/python

import requests
import sys
import data_handlers
import sqlite3
import os.path
from datetime import date, timedelta
import json

def main():
  if len(sys.argv) < 4:
    print "usage: read.py <url> <handler> <db_file_path>"
  else:
    prepare_tables(sys.argv[3])  
    print str(sys.argv[1])
    resp = requests.get(sys.argv[1],verify=False)
    #   print resp
    #  resp_json = resp.json()
    resp_json = json.loads(resp.content)
    handler = getattr(data_handlers,sys.argv[2])
    handler(resp_json,sys.argv[3])


def prepare_tables(database_file_path):
  if os.path.exists(database_file_path):
    print database_file_path +" found." 
  else:
    db = sqlite3.connect(database_file_path)
    db.execute ('CREATE TABLE IF NOT EXISTS EventGenres (id INT PRIMARY KEY, name TEXT)')
    for idx, val  in enumerate(['exhibition','film','concert']):
      key = idx+1
      db.execute("INSERT INTO EventGenres VALUES (?,?)",(key, val))

    db.execute ('CREATE TABLE IF NOT EXISTS EventDates (id TEXT,date TEXT)')

    db.execute ("CREATE TABLE IF NOT EXISTS Event (id TEXT UNIQUE PRIMARY KEY, startDate TEXT, endDate TEXT, time TEXT,"
                "img TEXT, link TEXT, title TEXT, desc TEXT, venue TEXT, genre int, type TEXT default 'crawl')")
    try:
      db.execute ("ALTER TABLE Event ADD COLUMN IF NOT EXISTS venuePlainText TEXT");
    except:
      print "table alter skipped"
    

    db.execute ("CREATE INDEX IF NOT EXISTS idx1 ON Event(Venue)")
    db.execute ("CREATE INDEX IF NOT EXISTS idx2 ON Event(Link)")
    db.execute ("CREATE INDEX IF NOT EXISTS idx_date ON Event(startDate)")
    db.execute ("CREATE INDEX IF NOT EXISTS idx2_date ON Event(endDate)")
    
    print database_file_path +" created." 

main()
