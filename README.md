# CutePetsAustin [@cutepetsaustin](https://twitter.com/cutepetsaustin)

A twitter bot that posts a random adoptable pet from PetHarbor.com shelter(s).

To make it work with your city, simply change the `shelters` in `credentials.py`. You can find your shelter ID by inspecting a URL on PetHarbor.com, e.g. Austin = ASTN, and Denver = DNVR.

Forked from [codeforamerica/CutePetsDenver](https://github.com/codeforamerica/CutePetsDenver).

Tweeting at [@cutepetsaustin](https://twitter.com/cutepetsaustin).

## Quickstart

1. Configure `credentials.py`
2. Install the dependencies `pip install -r requirements.txt`
3. Tweet a random adoptable pet `python meow.py`

## Setup

### Requirements

- python 2.7
- pip - https://pip.pypa.io/en/latest/
- virtualenv - http://virtualenv.readthedocs.org/en/latest/

### Installation

- Clone the repo `git clone git@github.com:open-austin/CutePetsAustin.git`
- Configure `credentials.py` with your PetHarbor.com Shelter ID(s), Twitter API Key and Access Token:
	```py
	shelters = ['ASTN', 'DNVR']  # PetHarbor.com shelter IDs
	twitter_api_key = 'XXXXX'
	twitter_api_secret = 'XXXXX'
	twitter_access_token = 'XXXXX'
	twitter_access_token_secret = 'XXXXX'
	```
- Optionally, create and activate a [virtual environment](http://virtualenv.readthedocs.org/en/latest/)
- Install the python dependencies with `pip install -r requirements.txt`
- Tweet a random adoptable pet with `python meow.py`
- Optionally, schedule a cron job to execute `meow.py` every few hours

### Twitter

1. Create a new Twitter app.
2. On the API key tab for the Twitter app, modify permissions so the app can `Read` and `Write`.
   Create an access token. On the API Key tab in Twitter for the app, click Create my access token. *Note: It's important to change permissions to `Read/Write` before generating the access token. The access token is keyed for the specific access level and will not be updated when changing permissions.*
4. Copy the `API Key` and `Access Token` into `credentials.py`

## License

The MIT License (MIT)
