TOP_DIR = ..
include $(TOP_DIR)/common.mk

MODELS = $(shell cat $(SCHEMA_JSON) | jq -r ".models | keys[] | ascii_downcase")

TESTDATA_JSON = $(addprefix testdata/, $(MODELS:=.json))
	
DATA_GENERATOR = $(TOP_DIR)/tools/generate_testdata.py

$(shell mkdir -p testdata)

all : generate

generate : testdata testscript

test : test-init test-add

debug :
	@echo MODELS are $(MODELS)
	@echo TESTDATA_JSON are $(TESTDATA_JSON)
	python3 $(TOP_DIR)/tools/generate_testdata.py \
		-m Device -o testdata/device.json $(SCHEMA_JSON)

testdata : $(TESTDATA_JSON)

testdata/%.json : $(SCHEMA_JSON) $(DATA_GENERATOR)
	python3 $(DATA_GENERATOR) -m $* -o $@ $<

#	amcli gentestdata -s $(SCHEMA_JSON) \
#		-o testdata $(WORK_DIR)/specs/*.json

testscript: testdata
	python3 $(TOP_DIR)/tools/generate_testscript.py \
		-o test_add_all.sh $(TOP_DIR)/work/schema/schema.json
	chmod +x test_add_all.sh

test-init:
	cp -f $(TOP_DIR)/.env .

test-add : test-init
	prove -v test_add_all.sh | tee test_add_all.log

test-get : test-add
	cd testdata && prove -v get.sh | tee get.log

test-update : test-get
	cd testdata && prove -v update.sh | tee update.log

test-delete : test-update
	cd testdata && prove -v delete.sh | tee delete.log

clean :
	rm -rf data/*
	rm -rf testdata/*
	rm -rf fixtures/*

.PHONY : \
	all clean test testdata debug

