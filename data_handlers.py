from datetime import date, timedelta 
import hashlib

def tentoonstellingen(resp,db_file_path,venue_map):
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
   
    event['location_tmp_id'] = "_".join([t['location']['name'].replace(" ","_"),t['location']['city'].replace(" ","_")])
    event['genre'] = 1 

    if len(t['urls']):
      link = t['urls'][0]
      for ur in t['urls']:
        event['desc'] = event['desc'] + ' || ' + ur

    else:
      link = 'https://www.vvv.nl/nl/activiteitenkaart/detail/'+t['trcid']

    event['link'] = link
     
    if 'startdate' in t['dates']:
      event['startdate'] = t['dates']['startdate']
      event['id'] = get_id(t['title'],link,event['startdate'])
      if 'enddate' in t['dates']:
        event['enddate'] = t['dates']['enddate']
    else: 
      if 'singles' in t['dates']:
        event['dates'] = t['dates']['singles']
        event['id'] = get_id(t['title'],link,event['dates'][0])
      else: 
        print 'event has no dates:' + event['title'].encode('utf-8')  
        
    if 'media' in t:
      event['img'] = t['media'][0]['url']
    
    if 'id' in event:
      events.append(event)

  save_events_to_db(events,db_file_path,venue_map)

# generic function for saving parsed events to database
def save_events_to_db(events,db_file_path, venue_map):
  print db_file_path
  print venue_map
  #db = sqlite3.connect(database_file_path) 
   
 


def get_id(title,link,startdate):
  pre_id = title+link+startdate
  identifier = hashlib.sha224(pre_id.encode('utf-8')).hexdigest()
  return identifier


