#!/bin/bash

set -ex

function_name="cute-pets-austin"
git_head=$(git rev-parse HEAD)

aws lambda update-function-code \
	--function-name $function_name \
	--zip-file fileb://bundle.zip

aws lambda publish-version \
    --function-name $function_name \
    --description $git_head
