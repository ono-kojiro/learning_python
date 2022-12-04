
URL = https://192.168.0.98:9200
INDEX = my_testcase-0001
PRETTY = ?pretty

JSONLFILE = input.jsonl

all : data upload

data :
	python3 json2jsonl.py -o input.jsonl input.json

upload :
	curl -n -H 'Content-Type: application/json' \
        -XPOST "$(URL)/$(INDEX)/_bulk" \
        --data-binary "@$(JSONLFILE)"

delete :
	curl -n -XDELETE $(URL)/$(INDEX)

dump :
	curl -n -H 'Content-Type: application/json' \
        -XGET "$(URL)/$(INDEX)/_search$(PRETTY)"

clean :
	$(MAKE) delete
	rm -f input.jsonl

.PHONY : \
    all clean test

