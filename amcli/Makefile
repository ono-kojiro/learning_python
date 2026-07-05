TOP_DIR = .
include $(TOP_DIR)/common.mk

all : init generate migrate
	
prepare :
	python3 -m pip install -r requirements.txt

install :
	python3 -m pip install -e .

help :
	@echo "usage: make TARGET"
	@echo "  target:"
	@echo "    prepare"
	@echo "    install"
	@echo ""
	@echo "    generate ( spec schema model admin view serializer "
	@echo "       fixture importer gentest )"
	@echo ""
	@echo "    migrate"
	@echo "    loaddata"
	@echo ""
	@echo "    start"
	@echo "    test"
	@echo ""
	@echo ""
	@echo "    clean"

init :
	$(MAKE) -C work init

pytest :
	cd unittest && pytest

spec :
	$(MAKE) -C components spec

schema:
	$(MAKE) -C components schema

generate :
	$(MAKE) -C components
	#$(MAKE) -C tests gentest
	$(MAKE) testdata 
	$(MAKE) testscript

migrate :
	$(MAKE) -C work migrate

loaddata :
	$(MAKE) -C work loaddata

start :
	$(MAKE) -C work start

stop :
	$(MAKE) -C work stop

restart :
	$(MAKE) -C work restart

#test :
#	$(MAKE) start
#	sleep 1
#	pytest -s
#	$(MAKE) stop

test : start pytest test-init test-add test-get test-update test-delete
#test : start pytest test-init test-add test-get test-update

testdata :
	amcli gentestdata -s $(SCHEMA_JSON) \
		-o tests/testdata work/specs/*.json

testscript:
	amcli gentestscript -o tests/testdata/add.sh --action add \
		-s $(SCHEMA_JSON) tests/testdata/*.json
	amcli gentestscript -o tests/testdata/get.sh --action get \
		-s $(SCHEMA_JSON) tests/testdata/*.json
	amcli gentestscript -o tests/testdata/update.sh --action update \
		-s $(SCHEMA_JSON) tests/testdata/*.json
	amcli gentestscript -o tests/testdata/delete.sh --action delete \
		-s $(SCHEMA_JSON) tests/testdata/*.json


test-init:
	echo "BASE_URL=https://localhost:8000" > tests/testdata/.env
	echo "CERTFILE=luna2.pem" >> tests/testdata/.env
	cp -f luna2.pem tests/testdata/
	cat tests/testdata/*.json

test-add :
	cd tests/testdata && sh add.sh

test-get :
	cd tests/testdata && sh get.sh

test-update :
	cd tests/testdata && sh update.sh

test-delete :
	cd tests/testdata && sh delete.sh

clean :
	$(MAKE) stop
	$(MAKE) -C components clean
	$(MAKE) -C work clean
	$(MAKE) -C tests clean

.PHONY : \
	all clean test schema

.EXPORT_ALL_VARIABLES:

