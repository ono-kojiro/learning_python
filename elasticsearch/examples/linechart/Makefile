include api_key.mk

BASE_URL = https://192.168.0.98:9200
INDEX = linechart
PRETTY = ?pretty


SPLIT_JSON = split_json.py

CURL_OPTS = -k -H 'Authorization: ApiKey $(ENCODED)' -H 'Content-type: application/json'

PRETTY = ?pretty

all : data

help:
	@echo "usage: make TARGET"
	@echo ""
	@echo "  target:"
	@echo "    help"
	@echo "    data"
	@echo ""
	@echo "    create"
	@echo "    delete"
	@echo "    upload"

data:
	python3 json2jsonl.py data.json > data.jsonl

create :
	curl $(CURL_OPTS) -XPUT $(BASE_URL)/$(INDEX)$(PRETTY)

delete :
	curl $(CURL_OPTS) -XDELETE $(BASE_URL)/$(INDEX)$(PRETTY)

upload:
	curl $(CURL_OPTS) \
        -XPOST "$(BASE_URL)/$(INDEX)/_bulk$(PRETTY)" \
        --data-binary "@data.jsonl"

dump :
	curl $(CURL_OPTS) -XGET "$(BASE_URL)/$(INDEX)/_search$(PRETTY)"

clean :
	$(MAKE) delete
	rm -f data.jsonl

.PHONY : \
    all clean test

