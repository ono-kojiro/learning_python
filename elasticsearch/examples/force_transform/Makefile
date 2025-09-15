# see https://vega.github.io/vega/docs/transforms/force/
#
include api_key.mk

BASE_URL = https://192.168.0.98:9200
INDEX = miserables
PRETTY = ?pretty


SPLIT_JSON = split_json.py
JSON2JSONL = json2jsonl.py

CURL_OPTS = -k -H 'Authorization: ApiKey $(ENCODED)' \
	-H 'Content-type: application/json'

PRETTY = ?pretty
	
URL_BASE = https://raw.githubusercontent.com/vega/vega
DATA_URL = $(URL_BASE)/refs/heads/main/docs/data/miserables.json
DATA_JSON = $(shell basename $(DATA_URL))
DATA_JSONL = $(DATA_JSON:.json=.jsonl)

all : data

debug :
	echo $(DATA_JSONL)

help:
	@echo "usage: make TARGET"
	@echo ""
	@echo "  target:"
	@echo "    help"
	@echo ""
	@echo "    create       create index"
	@echo "    delete       delete index"
	@echo ""
	@echo "    fetch        fetch original data"
	@echo "    data         create data"
	@echo "    upload       upload data"
	@echo ""
	@echo "    dump         dump data"

fetch:
	curl --silent -O $(DATA_URL)

data : jsonl
	
jsonl : $(DATA_JSONL)

%.jsonl : %.json
	python3 $(JSON2JSONL) -n $* $< > $@

create:
	curl $(CURL_OPTS) -XPUT $(BASE_URL)/$(INDEX)$(PRETTY)

delete :
	curl $(CURL_OPTS) -XDELETE $(BASE_URL)/$(INDEX)$(PRETTY)

upload : 
	curl $(CURL_OPTS) \
        -XPOST "$(BASE_URL)/$(INDEX)/_bulk$(PRETTY)" \
        --data-binary "@$(DATA_JSONL)"

dump :
	curl $(CURL_OPTS) -XGET "$(BASE_URL)/$(INDEX)/_search$(PRETTY)"

clean :
	rm -f $(DATA_JSONL)

mclean :
	$(MAKE) delete clean

.PHONY : \
    all clean test

