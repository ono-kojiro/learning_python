TOP_DIR = ..
include ../common.mk

MODELS_PY = $(addprefix $(MODEL_DIR)/, $(notdir $(SPECS_JSON:.json=_model.py)))

all : model copy

model : $(MODELS_PY)

$(MODEL_DIR)/%_model.py : $(SPEC_DIR)/%.json
	amcli genmodel -l $(TEMPLATE_DIR) -o $@ $<

copy :
	mkdir -p $(WORK_DIR)/$(APPLICATION)/models
	cp -f $(MODELS_PY) $(WORK_DIR)/$(APPLICATION)/models

clean :
	rm -f $(MODELS_PY)

