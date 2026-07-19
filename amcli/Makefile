TOP_DIR = .
include $(TOP_DIR)/common.mk
	
all : init generate admin_init migrate loaddata
	
prepare :
	if [ ! -d "myenv" ]; then \
		python3 -m venv myenv; \
	fi
	. ./myenv/bin/activate && python3 -m pip install -r requirements.txt

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
	cd tests/unittest && pytest

spec :
	$(MAKE) -C components spec

schema:
	$(MAKE) -C components schema

testschema:
	$(MAKE) -C components testschema

generate : init
	$(MAKE) -C components
	$(MAKE) -C tests generate

admin_init :
	python3 tools/generate_admin_init.py \
    	-o work/myapp/admin/__init__.py \
    	work/schema/schema.json
	#python3 tools/generate_through_spec.py \
	#	-o work/specs/through.json work/schema/schema.json
	#python3 tools/generate_through_model.py \
	#	-o work/myapp/models/through_models.py work/schema/schema.json

migrate : generate
	$(MAKE) -C work migrate

loaddata : generate migrate
	VERBOSE=1 $(MAKE) -C work loaddata

start :
	$(MAKE) -C work start

stop :
	$(MAKE) -C work stop

restart :
	$(MAKE) -C work restart
status :
	ps -aux | grep 'manage.py'

test :
	$(MAKE) start
	$(MAKE) pytest
	$(MAKE) -C tests test

clean :
	$(MAKE) stop
	$(MAKE) -C components clean
	$(MAKE) -C work clean
	$(MAKE) -C tests clean

.PHONY : \
	all clean test schema

.EXPORT_ALL_VARIABLES:

