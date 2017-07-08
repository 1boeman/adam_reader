#!/usr/bin/python

import requests
import sys
import data_handlers
import sqlite3

def main():
  prepare_tables(sys.argv[3])  
  if len(sys.argv) < 4:
    print "usage: read.py <url> <handler> <db_file_path>"
  else:
    print str(sys.argv[1])
    resp = requests.get(sys.argv[1],verify=False)
    resp_json = resp.json()
    handler = getattr(data_handlers,sys.argv[2])
    handler(resp_json,sys.argv[3])


def prepare_tables(database_file_path):
  db = sqlite3.connect(database_file_path)
  db.execute('CREATE TABLE IF NOT EXISTS EventDates (Id TEXT PRIMARY KEY,Date TEXT)')
  db.execute ("CREATE TABLE IF NOT EXISTS Event (Id TEXT PRIMARY KEY,Date TEXT,Time TEXT,"
              "Img TEXT, Link TEXT,Title TEXT,Desc TEXT,Venue TEXT, Type TEXT default 'crawl')")
  try:
    db.execute ("ALTER TABLE Event ADD COLUMN IF NOT EXISTS VenuePlaintext TEXT");
  except:
    print "table alter skipped"
  

  db.execute ("CREATE INDEX IF NOT EXISTS idx1 ON Event(Venue)")
  db.execute ("CREATE INDEX IF NOT EXISTS idx2 ON Event(Link)")
  db.execute ("CREATE INDEX IF NOT EXISTS idx_date ON Event(Date)")


main()
