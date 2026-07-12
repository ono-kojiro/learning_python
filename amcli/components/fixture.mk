# file: components/fixture.mk
TOP_DIR = ..
include ../common.mk

#FIXTURES_YML = $(addprefix $(FIXTURE_DIR)/, $(notdir $(SPECS_JSON:.json=_fixture.yaml)))
#FIXTURE_ORDER = remark device netif ipv4 manager os comment
#FIXTURES_YML = $(addprefix $(FIXTURE_DIR)/, $(addsuffix _fixture.yaml, $(FIXTURE_ORDER)))

FIXTURES_ALL_YML = $(FIXTURE_DIR)/fixture_all.yaml

$(shell mkdir -p $(FIXTURE_DIR))

all : fixture

#fixture : $(FIXTURES_YML)
fixture : $(FIXTURES_ALL_YML)

$(FIXTURE_DIR)/%_fixture.yaml : $(SPEC_DIR)/%.json
	amcli genfixture -o $@ -l $(TEMPLATE_DIR) -s $(SCHEMA_JSON) \
		-t $(TESTSCHEMA_JSON) \
		-n $(TEMPLATE_DIR)/names.yaml $<

$(FIXTURES_ALL_YML) : $(TESTSCHEMA_JSON) $(SPECS_JSON)
	python3 $(TOP_DIR)/tools/generate_fixture.py -o $@ $(SPECS_JSON)

clean :
	rm -f $(FIXTURES_ALL_YML)

