TOP_DIR = ..
include ../common.mk

$(shell mkdir -p $(SCHEMA_DIR))

all : schema

schema : $(SCHEMA_JSON)

$(SCHEMA_JSON) : $(SPECS_JSON)
	amcli genschema -o $@ \
		--project $(PROJECT) --application $(APPLICATION) $(SPECS_JSON) \
	2>&1 | tee amcli_genschema.log

clean :
	rm -rf $(SCHEMA_JSON)

