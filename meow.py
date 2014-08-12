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

    if four_oh_four in res.content:
        print 404, url
    else:
        print 200, url
        print res.content
        in_db = True
        media = 'lalalafind.theurl'  # FIXME: Figure out how to get the image url

    return in_db, media


intake_start_time = arrow.now().format('YYYY-MM-DD')
intake_end_time = arrow.now().replace(days=1).format('YYYY-MM-DD')  # Doubt there will be a date in the future, but just in case
url = "http://data.austintexas.gov/resource/5cgv-i2cu.json?$where=intake_type>='{}' AND intake_type<'{}'".format(intake_start_time, intake_end_time)
print 'GET', url
res = requests.get(url)
res.raise_for_status()
pets = res.json()
print 'Found {} pets'.format(len(pets))
existing_pets = []

for pet in pets:
    in_db, media = get_pet_details(pet['image_link']['url'])

    if in_db:
        existing_pets.append(pet)

print '{} of {} pets still exist in PetHarbor'.format(len(existing_pets), len(pets))

if existing_pets:
    lucky = random.choice(existing_pets)
    latlng = (lucky['found_location']['latitude'], lucky['found_location']['longitude'])
    status = '{} {} {} {}'.format(lucky['color'], lucky['looks_like'], lucky['type'], lucky['image_link']['url'])
    print 'Chosen one:', lucky
    # tweet(status, latlng, media)
