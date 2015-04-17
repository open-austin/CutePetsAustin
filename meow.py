#!/usr/bin/python
# -*- coding: utf-8 -*-

import json
import random
import re
from pprint import pprint

from bs4 import BeautifulSoup
import requests
from requests_oauthlib import OAuth1Session

from credentials import shelters, twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_token_secret

greetings = [
    "Hey! I'm",
    "¡Hola! Me llamo",
    "Hey there! I'm",
    "Hi! My name is",
    "Hello! I am",
    "Hello! I'm",
    "Hi! My name's",
    "I'm",
    "I am",
    "They call me",
    "Call me",
    "I'm",
    "Hello, I'm",
    "Hey, I'm",
    "HI! I'm",
    "HEY! I am"
]
greetings_no_name = [
    "Hey!",
    "¡Hola!",
    "Hey there!",
    "Hi!",
    "Hello!",
    "Howdy!",
    "Hey.",
    "HI!",
    "HEY!"
]


def tweet(status, latlng=None, media=None):
    twitter = OAuth1Session(twitter_api_key, twitter_api_secret, twitter_access_token, twitter_access_token_secret)
    url = 'https://api.twitter.com/1.1/statuses/update{}.json'.format('_with_media' if media else '')
    params = {'status': status}
    if latlng:
        params['lat'] = latlng[0]
        params['lon'] = latlng[1]
    files = {'media': media} if media else None

    print('POST', url, params)
    res = twitter.post(url=url, params=params, files=files)

    print(res.status_code, res.request.url)
    res.raise_for_status()
    data = res.json()
    pprint(data)

    return data


def fetch_petharbor_adoptable_pets(shelterlist, where):
    shelterlist = ','.join(["'{}'".format(s) for s in shelterlist])
    url = 'http://www.petharbor.com/results.asp'
    params = {
        'searchtype': 'ADOPT',
        'friends': '1',
        'samaritans': '1',
        'nosuccess': '0',
        'orderby': 'Days in Shelter',
        'rows': '10',
        'imght': '120',
        'imgres': 'thumb',
        'view': 'sysadm.v_austin',
        'nobreedreq': '1',
        'bgcolor': 'ffffff',
        'fontface': 'arial',
        'fontsize': '10',
        'col_hdr_bg': '29abe2',
        'col_hdr_fg': '29abe2',
        'col_fg': '29abe2',
        'SBG': 'ffffff',
        'zip': '78704',
        'miles': '10',
        'shelterlist': shelterlist,
        'atype': '',
        'where': where,
        'PAGE': '1',
    }

    print('GET', url)
    res = requests.get(url, params=params)

    print(res.status_code, res.request.url)
    res.raise_for_status()

    return res.content


def parse_petharbor_search_results(html):
    # returns (pet_id, shelter_id)
    pets = re.findall('ID=(A\d+)&LOCATION=(\w+)&', html)
    return pets


def fetch_petharbor_pet_details(pet_id, shelter_id):
    url = 'http://www.petharbor.com/pet.asp?uaid={}.{}'.format(shelter_id, pet_id)

    print('GET', url)
    res = requests.get(url)

    print(res.status_code, res.request.url)
    res.raise_for_status()

    return res.content


def parse_petharbor_pet_details(html, pet_id, shelter_id):
    soup = BeautifulSoup(html)

    # get the name
    name = soup.find('meta', attrs={'property': 'og:title'})['content']
    name = name.replace('*', '').title()
    # if name is This Cat/Pet/Other
    if 'this' in name.lower():
        name = None

    desc_el = soup.select(".DetailDesc")[0]

    # remove the font tag, it is the "name - #id" thing
    desc_el.find_all('font')[0].extract()

    # the rest of the elements are sentences describing the pet
    desc_children = [str(x) for x in desc_el.children]
    desc = ' '.join(desc_children)
    desc = re.sub('(<br>|<br/>|</br>|<BR>|<BR/>|</BR>)', ' ', desc)  # much wow
    desc = re.sub('\n', ' ', desc)
    desc = re.sub('\s+', ' ', desc).strip()

    pet_details = {
        'name': name,
        'desc': desc,
        'url': 'http://www.petharbor.com/pet.asp?uaid={}.{}'.format(shelter_id, pet_id)
    }

    return pet_details


def fetch_petharbor_pet_image(pet_id, shelter_id):
    url = 'http://www.petharbor.com/get_image.asp?RES=Detail&ID={}&LOCATION={}'.format(pet_id, shelter_id)
    print('GET', url)
    res = requests.get(url)

    print(res.status_code, res.url)
    res.raise_for_status()

    return res.content


def has_tweeted_pet_already(pet_id, shelter_id, tweeted_path='.tweeted.json'):
    try:
        with open(tweeted_path) as fh:
            data = json.loads(fh.read())
    except IOError:
        data = {'tweeted': []}

    if [pet_id, shelter_id] in data['tweeted']:
        return True
    else:
        data['tweeted'].append([pet_id, shelter_id])
        with open(tweeted_path, 'w+') as fh:
            fh.write(json.dumps(data))
        return False


def choose_pet(pets):
    random.shuffle(pets)
    for pet in pets:
        if not has_tweeted_pet_already(pet[0], pet[1]):
            return pet


def main():
    old_html = fetch_petharbor_adoptable_pets(shelters, 'age_o')
    young_html = fetch_petharbor_adoptable_pets(shelters, 'age_y')
    pet_ids = parse_petharbor_search_results(old_html) + parse_petharbor_search_results(young_html)

    print('Found {} potential pets {}'.format(len(pet_ids), pet_ids))

    pet = choose_pet(pet_ids)

    if not pet:
        print('All pets have already been tweeted')
        return

    print('Chose pet', pet)

    pet_details_html = fetch_petharbor_pet_details(pet[0], pet[1])
    pet_details = parse_petharbor_pet_details(pet_details_html, pet[0], pet[1])
    pet_image = fetch_petharbor_pet_image(pet[0], pet[1])

    print(pet_details['name'], pet_details['desc'])

    if pet_details['name']:
        tweet_format = '{greeting} {name}. {desc}… {url}'
        greeting = random.choice(greetings)
    else:
        tweet_format = '{greeting} {desc}… {url}'
        greeting = random.choice(greetings_no_name)

    status = tweet_format.format(
        greeting=greeting,
        name=pet_details['name'],
        desc=pet_details['desc'][:65],
        url=pet_details['url']
    )

    print('Le tweet ({} chars): {}'.format(len(status), status))

    tweet(status, media=pet_image)


if __name__ == '__main__':
    main()
