TOP_DIR = ..
include ../common.mk

$(shell mkdir -p $(TESTSCHEMA_DIR))

all : testschema

testschema : $(TESTSCHEMA_JSON)

$(TESTSCHEMA_JSON) : $(SCHEMA_JSON)
	amcli gentestschema -o $@ --schema $<

clean :
	rm -rf $(TESTSCHEMA_JSON)

