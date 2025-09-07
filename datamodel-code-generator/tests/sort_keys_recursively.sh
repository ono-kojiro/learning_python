#!/bin/sh

cat output.json | jq 'def walk(f): . as $in | if type == "object" then to_entries | map(.value |= walk(f)) | sort_by(.key) | from_entries elif type == "array" then map(walk(f)) else f end; walk(.)' > output-jq.json

cat Spec.json | jq 'def walk(f): . as $in | if type == "object" then to_entries | map(.value |= walk(f)) | sort_by(.key) | from_entries elif type == "array" then map(walk(f)) else f end; walk(.)' > Spec-jq.json


