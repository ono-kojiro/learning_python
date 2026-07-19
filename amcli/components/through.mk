TOP_DIR = ..
include ../common.mk

$(shell mkdir -p $(SCHEMA_DIR))

THROUGH_SPEC_JSON = $(SPEC_DIR)/devicemanager.json
THROUGH_MODEL_PY = $(MODEL_DIR)/devicemanager_model.py
	
GENERATE_SPEC  = $(TOP_DIR)/tools/generate_through_spec.py
GENERATE_MODEL = $(TOP_DIR)/tools/generate_through_model.py

all : spec model

spec : $(THROUGH_SPEC_JSON)

model : $(THROUGH_MODEL_PY)


$(THROUGH_SPEC_JSON) : $(SCHEMA_JSON) $(GENERATE_SPEC)
	python3 $(GENERATE_SPEC) -o $@ $<

$(THROUGH_MODEL_PY) : $(SCHEMA_JSON) $(GENERATE_MODEL)
	python3 $(GENERATE_MODEL) -o $@ $<

clean :
	rm -f $(THROUGH_SPEC_JSON)
	rm -f $(THROUGH_MODEL_PY)

