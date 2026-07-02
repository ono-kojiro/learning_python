TOP_DIR = ..

include ../common.mk

all : spec

spec : $(SPECS_JSON)

$(SPEC_DIR)/%.json : $(INPUT_DIR)/%.yml $(SPECS_YML)
	amcli cmp2ref --spec $< -o $@ $(SPECS_YML)

clean :
	rm -rf $(SPECS_JSON)

