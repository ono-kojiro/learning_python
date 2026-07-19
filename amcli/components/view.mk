TOP_DIR = ..
include ../common.mk

VIEWS_PY = \
	$(addprefix $(VIEW_DIR)/, $(notdir $(SPECS_JSON:.json=_view.py))) \
	$(VIEW_DIR)/devicemanager_view.py

$(shell mkdir -p $(VIEW_DIR))

all : view

view : $(VIEWS_PY)

$(VIEW_DIR)/%_view.py : $(SPEC_DIR)/%.json
	amcli genview -l $(TEMPLATE_DIR) -o $@ $<

clean :
	rm -f $(VIEWS_PY)

