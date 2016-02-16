import requests
import pprint
import csv
from config import EVENTBRITE_TOKEN

response = requests.get(
    "https://www.eventbriteapi.com/v3/events/search/?&venue.city=New_York&start_date.range_start=2016-02-22T00:00:00Z&categories=111&expand=venue,category",
    headers = {
        "Authorization": "Bearer "+EVENTBRITE_TOKEN,
    },
)

results = []
for i in range(0,5):
    result = {}
    result['name'] = response.json()['events'][i]['name']['text']
    result['url'] = response.json()['events'][i]['url']
    result['venue_long'] = response.json()['events'][i]['venue']['address']['longitude']
    result['venue_long'] = "{:.9f}".format(result['venue_long'])
    result['venue_lat'] = response.json()['events'][i]['venue']['address']['latitude']
    result['start_date'] = response.json()['events'][i]['start']['local']
    results.append(result)


with open('eventbrite.csv', 'wb') as csvfile:
    fieldnames = ['name', 'url', 'venue_long', 'venue_lat', 'start_date']
    spamwriter = csv.DictWriter(csvfile, fieldnames = fieldnames)
    spamwriter.writeheader()
    for result in results:
       spamwriter.writerow(result)
