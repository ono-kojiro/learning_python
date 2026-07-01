TOP_DIR = ..

include ../common.mk

SPECS_YML = $(wildcard $(SPEC_DIR)/*.yml)
SPECS_JSON = $(addprefix $(SPEC_DIR)/, $(notdir $(SPECS_YML:.yml=.json)))

all : spec copy

spec : $(SPECS_JSON)

$(SPEC_DIR)/%.json : $(SPEC_DIR)/%.yml
	amcli cmp2ref --spec $< -o $@ $(SPECS_YML)

copy :
	mkdir -p $(WORK_DIR)/specs
	cp -f $(SPECS_JSON) $(WORK_DIR)/specs/

clean :
	rm -rf $(SPECS_JSON)

