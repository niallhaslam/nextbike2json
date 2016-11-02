from xml.dom import minidom
import sys
import json
import requests
import shutil
import urllib
from uber_rides.session import Session
from uber_rides.client import UberRidesClient

CLIENT_SECRET = ''
SERVER_TOKEN = ''
ACCESS_TOKEN = ''
PRODUCT_ID = ''
OPENWEATHERAPPID = ''

CITYID = '238'

#if sys.argv[1] == '-':
#    tree = minidom.parse(sys.stdin)
#else:
#    tree = minidom.parse(sys.argv[1])

def getWeather(lat, lng):
    url = "http://api.openweathermap.org/data/2.5/weather?lat=" + lat + "&lon=" + lng + "&APPID=" + OPENWEATHERAPPID
    openweather = requests.get(url)
    print(url)
    print(openweather.text)
    weatherjson = json.loads(openweather.text)
    print(weatherjson['weather'])
    return weatherjson['weather']

def getlatlng(lat, lng):
    
    return [lat, lng]


def generate_ride_headers(token):
    """Generate the header object that is used to make api requests."""
    return {
        'Authorization': 'bearer %s' % token,
        'Content-Type': 'application/json',
    }

def getUberTime(lat,lng):
    server_token=SERVER_TOKEN

    #session auth loading
    querystring = {"start_latitude":lat,"start_longitude":lng}
    headers = {
    'authorization': "Token " + server_token,
    'cache-control': "no-cache",
    }
    url = 'http://api.uber.com/v1/'+ 'estimates/time'
    response = requests.request("GET", url,
        headers=headers, 
        params=querystring)
    print(lat)
    print(lng)
    print(response.text)
    return response

def estimate_ride(api_client):
    """Use an UberRidesClient to fetch a ride estimate and print the results.
    Parameters
        api_client (UberRidesClient)
            An authorized UberRidesClient with 'request' scope.
    """
    try:
        estimate = api_client.estimate_ride(
            product_id=PRODUCT_ID,
            start_latitude=START_LAT,
            start_longitude=START_LNG,
            end_latitude=END_LAT,
            end_longitude=END_LNG,
        )

    except (ClientError, ServerError) as error:
        fail_print(error)

    else:
        success_print(estimate.json)

with open('nboutput.txt', 'wb') as handle:
    nbfile = requests.get("https://nextbike.net/maps/nextbike-official.xml?city=" + CITYID, stream=True)

    for block in nbfile.iter_content(1024):
        handle.write(block)

tree = minidom.parse('nboutput.txt')

citylatlng = getlatlng(tree.childNodes[0].getElementsByTagName("city")[0].getAttribute("lat"), tree.childNodes[0].getElementsByTagName("city")[0].getAttribute("lng"))

currWeather = getWeather(citylatlng[0], citylatlng[1])
esttime = getUberTime(citylatlng[0], citylatlng[1])

places_list = {}
for place_elm in tree.childNodes[0].getElementsByTagName("place"):
    place = {"lat": place_elm.getAttribute("lat"),
             "lng": place_elm.getAttribute("lng"),
             "name": place_elm.getAttribute("name").strip(),
             "uid": int(place_elm.getAttribute("uid")),
             "weather": currWeather 
             }
    places_list[place['uid']] = place

#print(json.dumps(places_list))


