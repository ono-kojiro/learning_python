TOP_DIR = ..
include ../common.mk

all : schema

schema : $(SCHEMA_JSON)

$(SCHEMA_JSON) : $(SPECS_JSON)
	amcli genschema -o $@ \
		--project $(PROJECT) --application $(APPLICATION) $(SPECS_JSON)

clean :
	rm -rf $(SCHEMA_JSON)

