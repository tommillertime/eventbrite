import requests
import pprint
import csv

response = requests.get(
    "https://www.eventbriteapi.com/v3/events/search/?&venue.city=New_York&start_date.range_start=2016-02-22T00:00:00Z&categories=111&expand=venue,category",
    headers = {
        "Authorization": "Bearer Key",
    },
)
#pprint.pprint(response.json()['events'])
x = 2

for i in range(0,5):
    name = response.json()['events'][i]['name']['text']
    url = response.json()['events'][i]['url']
    venue_long = response.json()['events'][i]['venue']['address']['longitude']
    ven_long = "{:.9f}".format(venue_long)
    venue_lat = response.json()['events'][i]['venue']['address']['latitude']
    start_date = response.json()['events'][i]['start']['local']


    with open('eventbrite.csv', 'wb') as csvfile:
        fieldnames = ['name', 'url', 'venue_long', 'venue_lat', 'start_date']
        spamwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
        spamwriter.writeheader()
        spamwriter.writerow({'name': name, 'url' : url, 'venue_long': venue_long, 'venue_lat': venue_lat, 'start_date': start_date})
