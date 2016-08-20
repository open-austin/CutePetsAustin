#!/usr/bin/env bash

set -ex

rm -rf bundle bundle.zip

mkdir -p bundle

virtualenv_arg=$1

if [[ -n "$virtualenv_arg" ]]; then
    virtualenv=$1
else
    virtualenv=".env"
fi

/usr/bin/env bash $virtualenv/bin/activate
pip install -r requirements.txt

cp -r $virtualenv/lib/python2.7/site-packages/* bundle
cp *.py bundle
cd bundle

zip -rq9 ../bundle.zip *

cd ..

rm -rf bundle
