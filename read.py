#!/usr/bin/python

import requests
import sys

def main():
  if len(sys.argv) < 2:
    print "usage: read.py <url>"
  else:
    print str(sys.argv[1])
    resp = requests.get(sys.argv[1],verify=False)

    resp_json = resp.json()
    print resp_json.dumps()
main()


