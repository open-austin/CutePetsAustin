import random
import urlparse

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

    #  http://www.petharbor.com/pet.asp?uaid=ASTN.A685756 => ASTN, A685756
    params = urlparse.parse_qs(urlparse.urlparse(url).query)
    uaid = params['uaid'][0]
    location = uaid.split('.')[0]
    aid = uaid.split('.')[1]
    media_url = 'http://www.petharbor.com/get_image.asp?RES=Detail&ID={}&LOCATION={}'.format(aid, location)

    try:
        res = requests.get(media_url)
        print res.status_code, url
        res.raise_for_status()
        in_db = True
        media = res.content
    except:
        pass

    return in_db, media


intake_start_time = arrow.now().format('YYYY-MM-DD')
intake_end_time = arrow.now().replace(days=1).format('YYYY-MM-DD')  # Doubt there will be a date in the future, but just in case
url = "http://data.austintexas.gov/resource/5cgv-i2cu.json?$where=intake_type>='{}' AND intake_type<'{}'".format(intake_start_time, intake_end_time)
print 'GET', url
res = requests.get(url)
res.raise_for_status()
pets = res.json()
print 'Found {} pets'.format(len(pets))

lucky = random.choice(pets)
print 'Chosen one:', lucky

in_db, media = get_pet_details(lucky['image_link']['url'])

latlng = (lucky['found_location']['latitude'], lucky['found_location']['longitude'])
status = '{} {} {} {}'.format(lucky['color'], lucky['looks_like'], lucky['type'], lucky['image_link']['url'])
tweet(status, latlng, media)
