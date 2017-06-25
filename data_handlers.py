import sqlite3

def tentoonstellingen(resp):

  for t in resp:
    print t['trcid']
    print t['title']
    print t['location']['name']
    print t['location']
    print t['urls']
