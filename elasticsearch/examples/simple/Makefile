
URL = https://192.168.0.98:9200
INDEX = my_index-0001
PRETTY = ?pretty

all : data create upload

data :
	python3 xml2jsonl.py -o output.jsonl input.xml

create :
	curl -n -XPUT $(URL)/$(INDEX)

delete :
	curl -n -XDELETE $(URL)/$(INDEX)

upload :
	curl -n -H 'Content-Type: application/json' \
        -XPOST "$(URL)/$(INDEX)/_bulk" \
        --data-binary "@output.jsonl"

dump :
	curl -n -H 'Content-Type: application/json' \
        -XGET "$(URL)/$(INDEX)/_search$(PRETTY)"

clean :
	$(MAKE) delete
	rm -f output.jsonl

.PHONY : \
    all clean test

