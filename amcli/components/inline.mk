TOP_DIR = ..
include ../common.mk

INLINES_PY = $(addprefix $(ADMIN_DIR)/, $(notdir $(SPECS_JSON:.json=_inline.py)))

GENERATOR = $(TOP_DIR)/tools/generate_inline.py

$(shell mkdir -p $(ADMIN_DIR))

all : inline
	
inline : $(INLINES_PY)


$(ADMIN_DIR)/%_inline.py : $(SCHEMA_JSON)
	python3 $(GENERATOR) -o $@ -m $* $<

clean :
	rm -f $(INLINES_PY)

