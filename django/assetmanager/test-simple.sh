#!/bin/sh

url="https://127.0.0.1:8000/api/devices/"

show_devices()
{
  curl -k -s $url | jq
}

count_devices()
{
  curl -k -s $url | jq '. | length'
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


echo "1..4"

exp="0"
got=`count_devices`

if [ "$got" -eq "$exp" ]; then
  echo "DEBUG: $num"
  echo "ok - init"
else
  echo "not pk - init"
fi

add_devices

exp="3"
got=`count_devices`
if [ "$got" -eq "$exp" ]; then
  echo "DEBUG: $num"
  echo "ok - add1"
else
  echo "not pk - add1"
fi

add_devices
got=`count_devices`
exp="6"
if [ "$got" -eq "$exp" ]; then
  echo "DEBUG: $num"
  echo "ok - add2"
else
  echo "not pk - add2"
fi


delete_devices
got=`count_devices`
exp="0"
if [ "$got" -eq "$exp" ]; then
  echo "DEBUG: $num"
  echo "ok - delete"
else
  echo "not pk - delete"
fi



