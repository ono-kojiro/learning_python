TOP_DIR = ..
include ../common.mk

MODELS_PY = $(addprefix $(MODEL_DIR)/, $(notdir $(SPECS_JSON:.json=_model.py)))

$(shell mkdir -p $(MODEL_DIR))

all : model

model : $(MODELS_PY)

$(MODEL_DIR)/%_model.py : $(SPEC_DIR)/%.json
	amcli genmodel -l $(TEMPLATE_DIR) -o $@ $<

clean :
	rm -f $(MODELS_PY)

