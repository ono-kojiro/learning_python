TOP_DIR = .
include $(TOP_DIR)/common.mk

all : init generate migrate loaddata
	
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

generate :
	$(MAKE) -C components

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
	$(MAKE) start
	sleep 1
	pytest -s
	$(MAKE) stop

clean :
	$(MAKE) -C components clean
	$(MAKE) -C work clean

.PHONY : \
	all clean test schema

.EXPORT_ALL_VARIABLES:

