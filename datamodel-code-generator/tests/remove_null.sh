#!/bin/sh

cat output-jq.json | jq 'del(..|nulls)' > output-jq-null.json
cat Spec-jq.json | jq 'del(..|nulls)' > Spec-jq-null.json



