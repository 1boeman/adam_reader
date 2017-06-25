#!/usr/bin/python

import requests
import sys
import data_handlers

def main():
  if len(sys.argv) < 3:
    print "usage: read.py <url> <handler>"
  else:
    print str(sys.argv[1])
    resp = requests.get(sys.argv[1],verify=False)
    resp_json = resp.json()
    handler = getattr(data_handlers,sys.argv[2])
    handler(resp_json)

main()


