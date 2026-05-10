#!/bin/sh

top_dir="$( cd "$( dirname "$0" )" >/dev/null 2>&1 && pwd )"
cd $top_dir

if [ ! -f "./.env" ]; then
  echo "ERROR: no .env file in current directory" 1>&2
  exit 1
fi

. ./.env

flags=""

db="aozora"

help()
{
  cat << EOS
usage : $0 [options] target1 target2 ...

  target:
    create
    ls
EOS

}

all()
{
  ls
}

device()
{
   curl -s -k -X POST https://${DEX_HTTPS}/dex/device/code \
     -d "client_id=myclient" \
     -d "scope=openid email profile groups offline_access" \
   | jq . | tee device_code.json
}

auth()
{
   verification_uri_complete=`cat device_code.json \
     | jq -r ".verification_uri_complete"`
   lynx ${verification_uri_complete}
}

refresh()
{
  code=`cat device_code.json | jq -r ".device_code"`
  client_id="myclient"
  grant_type="urn:ietf:params:oauth:grant-type:device_code"
  curl -k -s -X POST https://${DEX_HTTPS}/dex/token \
          -d "grant_type=$grant_type" \
          -d "device_code=$code" \
          -d "client_id=$client_id" | jq . | tee refresh_token.json
}

access()
{
  ref=`cat refresh_token.json | jq -r ".refresh_token"`

  curl -k -s \
    -X POST https://${DEX_HTTPS}/dex/token \
    -d "grant_type=refresh_token" \
    -d "refresh_token=$ref" \
    -d "client_id=myclient" | jq . | tee access_token.json
}

session()
{
  token=`cat access_token.json | jq -r ".access_token"`

  curl -s -k \
    -H "Authorization: Bearer $token" \
    https://${COUCHDB_HTTPS}/_session | jq . | tee session.json
}

create()
{
   curl -s \
   -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} \
   -X PUT https://${COUCHDB_HTTPS}/aozora
}

delete()
{
   curl -s \
   -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} \
   -X DELETE https://${COUCHDB_HTTPS}/aozora
}

security()
{
  name=`cat session.json | jq -r '.userCtx.name'`

  data=`cat << EOF
  {
    "admins": {
      "names": [ "$name" ],
      "roles": [ "_admins" ]
    },
    "members": {
      "names": [ "$name" ],
      "roles": [ "developer" ]
    }
  }
EOF
`
  curl -s -X PUT \
    -u ${COUCHDB_USER}:${COUCHDB_PASSWORD} \
    -H "Content-Type: Application/json" \
    https://${COUCHDB_HTTPS}/${db}/_security \
    -d "${data}"
}

add()
{
  token=`cat access_token.json | jq -r ".access_token"`
  #htmlfiles=`ls -1 *.html`
  htmlfiles=`find ./ -maxdepth 1 -name "*.html"`
  for htmlfile in $htmlfiles; do
    basename=`basename -s .html $htmlfile`
    jsonfile="${basename}.json"
    echo $jsonfile
    doc=`cat $jsonfile | jq -r '.title'`
    echo $doc
    curl -s -H "Authorization: Bearer $token" \
      -X PUT https://${COUCHDB_HTTPS}/${db}/$doc \
      -d @${jsonfile}
  done
}

args=""
while [ "$#" -ne 0 ]; do
  case $1 in
    -h )
      help
      exit 1
      ;;
    -v )
      verbose=1
      ;;
    -* )
      flags="$flags $1"
      ;;
    * )
      args="$args $1"
      ;;
  esac
  
  shift
done

if [ -z "$args" ]; then
  help
  exit 1
fi

for target in $args; do
  target=`echo $target | tr '-' '_'`
  num=`LANG=C type $target 2>&1 | grep 'function' | wc -l`
  if [ "$num" -ne 0 ]; then
    $target
  else
    echo "ERROR : $target is not shell function"
    exit 1
  fi
done

