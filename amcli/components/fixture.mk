# file: components/fixture.mk
TOP_DIR = ..
include ../common.mk

#FIXTURES_YML = $(addprefix $(FIXTURE_DIR)/, $(notdir $(SPECS_JSON:.json=_fixture.yaml)))
FIXTURE_ORDER = remark device netif ipv4 manager os comment
FIXTURES_YML = $(addprefix $(FIXTURE_DIR)/, $(addsuffix _fixture.yaml, $(FIXTURE_ORDER)))

$(shell mkdir -p $(FIXTURE_DIR))

all : fixture

fixture : $(FIXTURES_YML)

$(FIXTURE_DIR)/%_fixture.yaml : $(SPEC_DIR)/%.json
	amcli genfixture -o $@ -l $(TEMPLATE_DIR) -s $(SCHEMA_JSON) \
		-n $(TEMPLATE_DIR)/names.yaml $<

clean :
	rm -f $(FIXTURES_YML)

