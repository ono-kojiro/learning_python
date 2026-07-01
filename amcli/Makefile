TOP_DIR = .
include $(TOP_DIR)/common.mk

all : init generate migrate loaddata
	
env :
	python3 -m venv myenv
	. ./myenv/bin/activate && pip3 install -r requirements.txt

install :
	. ./myenv/bin/activate && pip3 install -e .

init :
	$(MAKE) -C $(WORK_DIR) init

generate :spec schema model admin view serializer fixture importer

help :
	@echo "usage: make TARGET"
	@echo "  target:"
	@echo "    init"
	@echo "    generate ( spec schema model admin view serializer "
	@echo "       fixture importer )"
	@echo ""
	@echo "    clean"
spec :
	$(MAKE) -C specs

schema:
	$(MAKE) -C schema

model :
	$(MAKE) -C models

admin :
	$(MAKE) -C admins

view :
	$(MAKE) -C views

serializer :
	$(MAKE) -C serializers

fixture :
	$(MAKE) -C fixtures

importer :
	$(MAKE) -C importers

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

gentest :
	$(MAKE) -C tests gentest

test :
	pytest -s

clean :
	$(MAKE) -C importers clean
	$(MAKE) -C fixtures clean
	$(MAKE) -C serializers clean
	$(MAKE) -C views   clean
	$(MAKE) -C admins  clean
	$(MAKE) -C models  clean
	$(MAKE) -C schema  clean
	$(MAKE) -C specs   clean
	$(MAKE) -C work clean

.PHONY : \
	all clean test schema

.EXPORT_ALL_VARIABLES:

