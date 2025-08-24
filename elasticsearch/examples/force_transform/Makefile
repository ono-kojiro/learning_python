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

NODES_JSON  = nodes.json
NODES_JSONL = nodes.jsonl

LINKS_JSON  = links.json
LINKS_JSONL = links.jsonl

JSONFILES  = $(NODES_JSON)  $(LINKS_JSON)
JSONLFILES = $(NODES_JSONL) $(LINKS_JSONL) 

all : data

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

data : json jsonl
	
json  : $(JSONFILES)
	
jsonl : $(JSONLFILES)

%.json : $(DATA_JSON)
	python3 $(SPLIT_JSON) -n $* $< > $@

%.jsonl : %.json
	python3 $(JSON2JSONL) -n $* $< > $@

create:
	curl $(CURL_OPTS) -XPUT $(BASE_URL)/$(INDEX)$(PRETTY)

delete :
	curl $(CURL_OPTS) -XDELETE $(BASE_URL)/$(INDEX)$(PRETTY)

upload : upload_nodes upload_links

upload_nodes:
	curl $(CURL_OPTS) \
        -XPOST "$(BASE_URL)/$(INDEX)/_bulk$(PRETTY)" \
        --data-binary "@nodes.jsonl"

upload_links:
	curl $(CURL_OPTS) \
        -XPOST "$(BASE_URL)/$(INDEX)/_bulk$(PRETTY)" \
        --data-binary "@links.jsonl"

dump :
	curl $(CURL_OPTS) -XGET "$(BASE_URL)/$(INDEX)/_search$(PRETTY)"

clean :
	rm -f $(JSONFILES) $(JSONLFILES)

mclean :
	$(MAKE) delete clean

.PHONY : \
    all clean test $(DATA_JSON)

