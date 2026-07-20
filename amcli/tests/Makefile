TOP_DIR = ..
include $(TOP_DIR)/common.mk

MODELS = $(shell cat $(SCHEMA_JSON) | jq -r ".models | keys[] | ascii_downcase")

TESTDATA_JSON = $(addprefix testdata/, $(MODELS:=.json))

$(shell mkdir -p testdata)

all : generate

generate : testdata testscript

test : test-init test-add test-get test-update test-delete

debug :
	@echo MODELS are $(MODELS)
	@echo TESTDATA_JSON are $(TESTDATA_JSON)
	python3 $(TOP_DIR)/tools/generate_testdata.py \
		-m Device -o testdata/device.json $(SCHEMA_JSON)

testdata : $(TESTDATA_JSON)

testdata/%.json : $(SCHEMA_JSON)
	python3 $(TOP_DIR)/tools/generate_testdata.py \
		-m $* -o testdata/$*.json $(SCHEMA_JSON)

#	amcli gentestdata -s $(SCHEMA_JSON) \
#		-o testdata $(WORK_DIR)/specs/*.json

testscript: testdata
	amcli gentestscript -o testdata/add.sh --action add \
		-s $(SCHEMA_JSON) testdata/*.json
	amcli gentestscript -o testdata/get.sh --action get \
		-s $(SCHEMA_JSON) testdata/*.json
	amcli gentestscript -o testdata/update.sh --action update \
		-s $(SCHEMA_JSON) testdata/*.json
	amcli gentestscript -o testdata/delete.sh --action delete \
		-s $(TESTSCHEMA_JSON) testdata/*.json

test-init:
	cp -f $(TOP_DIR)/.env testdata/
	echo "BASE_URL=https://localhost:8000" >> testdata/.env

test-add : test-init
	cd testdata && prove add.sh | tee add.log

test-get : test-add
	cd testdata && prove get.sh | tee get.log

test-update : test-get
	cd testdata && prove update.sh | tee update.log

test-delete : test-update
	cd testdata && prove delete.sh | tee delete.log

clean :
	rm -rf data
	rm -rf testdata
	rm -rf fixtures

.PHONY : \
	all clean test testdata debug

