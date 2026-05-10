include .env

HTTPS_DEX     = https://192.168.1.98:5554
HTTPS_COUCHDB = https://192.168.1.98:6984
#HTTPS_COUCHDB = https://192.168.1.98/couchdb

HTMLFILES = 57228_58735.html \
			56680_62855.html 56669_58756.html 56689_63891.html \
			57108_60897.html 56684_65242.html
TEXTFILES = $(HTMLFILES:.html=.txt)
NDJSONFILES = $(sort $(TEXTFILES:.txt=.ndjson))
JSONFILES = $(sort $(HTMLFILES:.html=.json))

ENCODED   = ZGxhZzhKMEI0bmtmYkpqZGx1ZFA6TWk5ZW1EblRFejdfZ1YwRUtkNWt4dw==

all : json

help :
	sh build.sh help

html:
	$(MAKE) -C html fetch

fetch : html

text : $(TEXTFILES)

json :
	$(MAKE) -C json json

ndjson : $(NDJSONFILE)

%.txt : %.html
	html2text -from_encoding sjis -o $@ $<

%.ndjson : %.txt
	python3 txt2ndjson.py -o $@ $<

prepare-vector :
	python3 txt2ndjson.py -o vector.json query.txt

prepare-query :
	jq --slurpfile vec vector.json \
  		'.knn.query_vector = $$vec[0].vector' \
  		template.json > query.json
  		
#'.query.script_score.script.params.query_vector = $$vec[0].vector' \

query :
	@curl -X POST "https://192.168.1.72:9200/embeddings-*/_search?pretty" \
		-H "Authorization: ApiKey $(ENCODED)" \
		-H "Content-Type: application/json" \
		--data-binary @query.json

check:
	curl -X GET "https://192.168.1.72:9200/embeddings-*/_mapping?pretty" \
		-H "Authorization: ApiKey $(ENCODED)" \

%.json : %.html
	python3 html2json.py -o $@ $<

createdb :
	curl -s -k -u $(COUCHDB_USER):$(COUCHDB_PASSWORD) \
		-X PUT $(HTTPS_COUCHDB)/aozora

upload :
	token=`cat access_token.json | jq -r '.access_token'`; \
	echo "DEBUG: token is $${token}"
	for jsonfile in $(JSONFILES) ; do \
		echo "jsonfile is $${jsonfile}"; \
		doc=`cat $${jsonfile} | jq -r '.title'`; \
		echo "doc is $${doc}"; \
		curl -s -k \
	 		-H "Autorization: Bearer $${token}" \
		  	-X PUT "$(HTTPS_COUCHDB)/aozora/$${doc}" \
		  	-d "@$${jsonfile}"; \
	done
device:
	curl -s -k -X POST $(HTTPS_DEX)/dex/device/code \
		-d "client_id=myclient" \
		-d "scope=openid email profile groups offline_access" \
    | jq . > device_code.json

auth :
	lynx `cat device_code.json | jq -r '.verification_uri_complete'`

refresh :
	device_code=`cat device_code.json | jq -r '.device_code'`; \
	client_id="myclient"; \
	grant_type="urn:ietf:params:oauth:grant-type:device_code"; \
	curl -k -s -X POST $(HTTPS_DEX)/dex/token \
	  -d "grant_type=$${grant_type}" \
	  -d "device_code=$${device_code}" \
	  -d "client_id=$${client_id}" | jq . > refresh_token.json

access:
	refresh_token=`cat refresh_token.json | jq -r '.refresh_token'`; \
	client_id="myclient"; \
	grant_type="refresh_token"; \
	curl -k -s -X POST $(HTTPS_DEX)/dex/token \
	  -d "grant_type=$${grant_type}" \
	  -d "refresh_token=$${refresh_token}" \
	  -d "client_id=$${client_id}" | jq . > access_token.json

session:
	access_token=`cat access_token.json | jq -r '.access_token'`; \
	echo "access_token is $${access_token}"; \
	curl -s -k \
	  -H "Authorization: Bearer $${access_token}" \
	  $(HTTPS_COUCHDB)/_session

without_access:
	curl -s -k $(HTTPS_COUCHDB)/_session

clean :
	rm -f $(TEXTFILES) $(JSONFILES)

.PHONY : \
	all clean test fetch json
