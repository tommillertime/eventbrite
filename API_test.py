import requests
response = requests.get(
    "https://www.eventbriteapi.com/v3/events/search/?&venue.city=New_York&start_date.range_start=2016-13-15T00:00:00Z",
    headers = {
        "Authorization": "Bearer ORQZ3DG2UZYWRAX77NJW",
    },
)
print response.json()['events'][0]['name']['text']

