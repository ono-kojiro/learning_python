#REF_YAMLS
#TOP_DIR

SCHEMA_YAML = schema.yaml

ifeq ($(TOP_DIR),)
	TOP_DIR = ..
endif

ifeq ($(REF_YAMLS),)
	REF_YAMLS = $(wildcard $(TOP_DIR)/template/app/*_ref.yaml)
endif

all: schema depend category

schema:
	@echo $(REF_YAMLS)
	@echo This is all.
	@echo TOP_DIR is $(TOP_DIR)
	./generate_schema.py -o $(SCHEMA_YAML) $(REF_YAMLS)

depend:
	./generate_depend.py -o depend.yaml schema.yaml

category:
	./generate_category.py -o category.yaml schema.yaml

