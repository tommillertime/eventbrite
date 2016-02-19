import requests
import pprint
import csv
from config import EVENTBRITE_TOKEN
import psycopg2
from config import PW_Stuff

conn = psycopg2.connect(PW_Stuff)

response = requests.get(
    "https://www.eventbriteapi.com/v3/events/search/?&venue.city=New_York&start_date.range_start=2016-02-22T00:00:00Z&start_date.range_end=2016-02-29T00:00:00Z&categories=113&expand=venue,category",
    headers = {
        "Authorization": "Bearer "+EVENTBRITE_TOKEN,
    },
)

results = []
for i in range(0,100):
    try:
        result = {}
        result['name'] = response.json()['events'][i]['name']['text']
        result['url'] = response.json()['events'][i]['url']
        result['venue_long'] = response.json()['events'][i]['venue']['address']['longitude']
        result['venue_lat'] = response.json()['events'][i]['venue']['address']['latitude']
        result['venue_address'] = response.json()['events'][i]['venue']['address']['address_1']
        result['start_date'] = response.json()['events'][i]['start']['local']

        venue_long2 = response.json()['events'][i]['venue']['address']['longitude']
        venue_lat2 = response.json()['events'][i]['venue']['address']['latitude']
        cur = conn.cursor()
        sql = "select location_slugs.slug from admin.adhoc_active_locations left join admin.location_slugs on location_slugs.location_id=adhoc_active_locations.id where ST_DWithin(coordinates, ST_GeogFromText('POINT(%s %s)'), 300)"
        data = (venue_long2, venue_lat2) # NOTE: This is longitude, latitude
        print data
        cur.execute(sql, data)
        result['nearest_garage'] = cur.fetchone()
        #print nearest_garage

        results.append(result)
    except:
        continue


with open('eventbrite.csv', 'wb') as csvfile:
    fieldnames = ['name', 'url', 'venue_long', 'venue_lat','venue_address', 'start_date', 'nearest_garage']
    spamwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
    spamwriter.writeheader()
    for result in results:
        try:
            spamwriter.writerow(result)
        except:
            print "program complete"
