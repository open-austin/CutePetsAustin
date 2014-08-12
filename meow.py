import random

import arrow
import requests
from requests_oauthlib import OAuth1Session

from credentials import client_key, client_secret, resource_owner_key, resource_owner_secret


def tweet(status, latlng, media=None):
    twitter = OAuth1Session(client_key, client_secret, resource_owner_key, resource_owner_secret)
    url = 'https://api.twitter.com/1.1/statuses/update{}.json'.format('_with_media' if media else '')
    params = {'status': status, 'lat': latlng[0], 'lon': latlng[1]}
    files = {'media': media} if media else None
    res = twitter.post(url=url, params=params, files=files)
    res.raise_for_status()
    print res.json()


def get_pet_details(url):
    in_db = False
    media = None

    res = requests.get(url)
    res.raise_for_status()

    four_oh_four = 'Sorry!  This animal is no longer in our online database.  Please check with the shelter to see about its availability.'
    if four_oh_four not in res.content:
        print res.content
        in_db = True
        media = 'lalalafind.theurl'

    return in_db, media


intake_start_time = arrow.now().replace(hours=-2).isoformat()
url = "http://data.austintexas.gov/resource/5cgv-i2cu.json?$where=intake_type>='{}'".format(intake_start_time)
print 'GET', url
res = requests.get(url)
pets = res.json()
potential_pets = []

for pet in pets:
    in_db, media = get_pet_details(url)

    if in_db:
        potential_pets.append(pet)

if not potential_pets:
    print 'No pets found'
else:
    lucky = random.choice(potential_pets)
    latlng = (lucky['found_location']['latitude'], lucky['found_location']['longitude'])
    status = '{} {} {} {}'.format(lucky['color'], lucky['looks_like'], lucky['type'], lucky['image_link']['url'])
    print 'Chosen one:', lucky
    tweet(status, latlng, media)
