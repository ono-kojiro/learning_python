#!/bin/sh

url="https://127.0.0.1:8000/api/devices/"

show_devices()
{
  curl -k -s $url | jq
}

add_devices()
{
  devids="1 2 3"
  for devid in $devids; do
    name="Device${devid}"

    curl -k -s -X POST $url \
      -H "Content-Type: application/json" \
      -d "{ \"name\": \"$name\", \"serial_number\": \"ABC123\"}" | jq

  done
}

delete_devices()
{
  devids=`curl -k -s $url | jq ".[].id" -r`
  for devid in $devids; do
    curl -k -s -X DELETE ${url}${devid}/
  done
}

show_devices
add_devices
delete_devices
show_devices




