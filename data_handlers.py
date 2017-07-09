
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
    if len(t['urls']):
      link = t['urls'][0]
    else:
      link = 'https://www.vvv.nl/nl/activiteitenkaart/detail/'+t['trcid']
    print t['dates']
    
    dates = get_dates_between()
    print [title,location,desc,link]


def get_dates_between(start_date,end_date):
    d1 = date(2008, 8, 15)  # start date
  d2 = date(2008, 9, 15)  # end date

  delta = d2 - d1         # timedelta

  for i in range(delta.days + 1):
    print(d1 + timedelta(days=i))
