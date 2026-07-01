TOP_DIR = ..
include ../common.mk

FIXTURES_YML = $(addprefix $(FIXTURE_DIR)/, $(notdir $(SPECS_JSON:.json=_fixture.yaml)))

all : fixture copy

fixture : $(FIXTURES_YML)

$(FIXTURE_DIR)/%_fixture.yaml : $(SPEC_DIR)/%.json
	amcli genfixture -o $@ -l $(TEMPLATE_DIR) -s $(SCHEMA_JSON) \
		-n $(TEMPLATE_DIR)/names.yaml $<

copy :
	mkdir -p $(TEST_DIR)/data
	cp -f $(FIXTURES_YML) $(TEST_DIR)/data

clean :
	rm -f $(FIXTURES_YML)

