import re
from datetime import date, timedelta 
import hashlib
import sqlite3

def tentoonstellingen(resp,db_file_path):
  events = []
  for t in resp:
   # print t['trcid']
    event = {   
      'title': t['title'],
    }
    
    location = ", ".join([t['location']['name'], t['location']['adress'], t['location']['city']])
    
    event['desc'] =  " || ".join( [location,t['details']["en"]["calendarsummary"],
                        t['details']["en"]["shortdescription"],
                        t['details']["nl"]["shortdescription"]] )

    if not len(t['location']['name']):
      continue

    event['venue'] = "_".join([t['location']['name'].replace(" ","_"),t['location']['city'].replace(" ","_")]).lower()
    event['genre'] = 1 

    if len(t['urls']):
      link = t['urls'][0]
      for ur in t['urls']:
        event['desc'] = event['desc'] + ' || ' + ur

    else:
      link = 'https://www.vvv.nl/nl/activiteitenkaart/detail/'+t['trcid']

    event['link'] = link
     
    if 'startdate' in t['dates']:
      event['startDate'] = t['dates']['startdate']
      if 'enddate' in t['dates']:
        event['endDate'] = t['dates']['enddate']
    else: 
      if 'singles' in t['dates']:
        event['dates'] = t['dates']['singles']
        event['startDate'] = event['dates'][0]
      else: 
        print 'event has no dates:' + event['title'].encode('utf-8')  
    
    if 'startDate' in event:
      event['id'] = get_id(t['title'],event['venue'],event['startDate'])
    else:
      continue
    
    
    if 'media' in t:
      event['img'] = t['media'][0]['url']
    
    if 'id' in event:
      events.append(event)

  save_events_to_db(events,db_file_path)

# generic function for saving parsed events to database
def save_events_to_db(events,db_file_path):
  print db_file_path
  #mydoc = ElementTree(file=venue_map)
#  for e in mydoc.findall('/foo/bar'):
 #     print e.get('title').text
  
  db = sqlite3.connect(db_file_path) 
  nullables = ['startDate','endDate','time','img']
  for event in events:
    for nullable in nullables:
      if nullable not in event:
        event[nullable] = ''
      
    values = (
      event['id'],
      event['startDate'],
      event['endDate'],
      event['time'],
      event['img'], 
      event['link'],
      event['title'],
      event['desc'],
      event['venue'],
      event['genre'],
      None
    )
    try:
      db.execute('insert into Event values (?,?,?,?,?,?,?,?,?,?,?)',values)
    except Exception as e:
      print(e)
      print values
      continue

    if 'dates' in event:
      for dat in event['dates']:
        db.execute('insert into EventDates values(?,?)',[event['id'],dat])
    db.commit() 


def get_id(title,place,startdate):
  pre_id = "_".join([title,place,startdate]).lower()

  pre_id = re.sub('\W+', '_', pre_id)
 
  return pre_id
  #identifier = hashlib.sha224(pre_id.encode('utf-8')).hexdigest()
  #return identifier


