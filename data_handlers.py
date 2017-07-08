
def tentoonstellingen(resp,db_file_path):

  for t in resp:
    print t['trcid']
    title = t['title']
    location = ", ".join([t['location']['name'], t['location']['adress'], t['location']['city']])
    print t['urls']
    desc = " || ".join([t['details']["en"]["calendarsummary"],
                        t['details']["en"]["shortdescription"],
                        t['details']["nl"]["shortdescription"]] )
    for u in t['urls']:
      desc = desc + ' || ' + u

    link = 'https://www.vvv.nl/nl/activiteitenkaart/detail/'+t['trcid']

    
    print [title,location,desc,link]

