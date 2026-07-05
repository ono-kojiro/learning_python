TOP_DIR = ../
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
		-s $(SCHEMA_JSON) testdata/*.json

test-init:
	echo "BASE_URL=https://localhost:8000" > testdata/.env
	cat testdata/*.json

test-add :
	cd testdata && sh add.sh

test-get :
	cd testdata && sh get.sh

test-update :
	cd testdata && sh update.sh

test-delete :
	cd testdata && sh delete.sh

clean :
	rm -rf data
	rm -rf testdata

.PHONY : \
	all clean test testdata

