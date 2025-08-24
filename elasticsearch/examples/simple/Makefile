include api_key.mk

BASE_URL = https://192.168.0.98:9200
INDEX = myindex
PRETTY = ?pretty


CURL_OPTS = -k -H 'Authorization: ApiKey $(ENCODED)' -H 'Content-type: application/json'

PRETTY = ?pretty

all : data create upload

data :
	python3 xml2jsonl.py -o output.jsonl input.xml

create :
	curl $(CURL_OPTS) -XPUT $(BASE_URL)/$(INDEX)$(PRETTY)

delete :
	curl $(CURL_OPTS) -XDELETE $(BASE_URL)/$(INDEX)$(PRETTY)

upload :
	curl $(CURL_OPTS) \
        -XPOST "$(BASE_URL)/$(INDEX)/_bulk$(PRETTY)" \
        --data-binary "@output.jsonl"

dump :
	curl $(CURL_OPTS) -XGET "$(BASE_URL)/$(INDEX)/_search$(PRETTY)" | \
		jq ".hits.hits"

clean :
	$(MAKE) delete
	rm -f output.jsonl

.PHONY : \
    all clean test

