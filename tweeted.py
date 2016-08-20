#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import print_function

import json

import boto3
import botocore


BUCKET = 'cute-pets-austin'
KEY = 'tweeted.json'


def get_tweeted_from_s3(bucket=BUCKET, key=KEY):
    print('Getting tweeted object from s3://{}/{}'.format(bucket, key))
    s3 = boto3.resource('s3')
    obj = s3.Object(bucket, key)
    try:
        res = obj.get()
        data = json.load(res['Body'])
        print('Succcessfuly loaded tweeted object')
    except botocore.exceptions.ClientError:
        # obj probably doesn't exist
        print('Tweeted object did\'t exist, starting with empty one')
        data = {'tweeted': []}

    return data


def put_tweeted_to_s3(data, bucket=BUCKET, key=KEY):
    print('Putting tweeted object to s3://{}/{}'.format(bucket, key))
    s3 = boto3.resource('s3')
    s3.Object(bucket, key).put(Body=json.dumps(data))
