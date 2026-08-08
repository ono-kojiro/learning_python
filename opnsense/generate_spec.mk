TOP_DIR = ..

include controllers.mk
include $(TOP_DIR)/variables.mk

all : spec

spec : $(SPECS_YML)

$(SPEC_DIR)/%.yml : $(SOURCE_DIR)/%controller.php
	mkdir -p `dirname $@`
	python3 $(TOP_DIR)/php2yml.py -o $@ $<

