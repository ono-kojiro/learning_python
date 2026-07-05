TOP_DIR = ..
include $(TOP_DIR)/common.mk

all : generate

generate : testdata testscript

test : test-init test-add test-get test-update test-delete

testdata :
	amcli gentestdata -s $(SCHEMA_JSON) \
		-o testdata $(WORK_DIR)/specs/*.json

testscript:
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

test-add :
	cd testdata && prove add.sh

test-get :
	cd testdata && prove get.sh

test-update :
	cd testdata && prove update.sh

test-delete :
	cd testdata && prove delete.sh

clean :
	rm -rf data
	rm -rf testdata

.PHONY : \
	all clean test testdata

