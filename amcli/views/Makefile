TOP_DIR = ..
include ../common.mk

VIEWS_PY = $(addprefix $(VIEW_DIR)/, $(notdir $(SPECS_JSON:.json=_view.py)))

all : view copy

view : $(VIEWS_PY)

$(VIEW_DIR)/%_view.py : $(SPEC_DIR)/%.json
	amcli genview -l $(TEMPLATE_DIR) -o $@ $<

copy :
	mkdir -p $(WORK_DIR)/$(APPLICATION)/views
	cp -f $(VIEWS_PY) $(WORK_DIR)/$(APPLICATION)/views/

clean :
	rm -f $(VIEWS_PY)

