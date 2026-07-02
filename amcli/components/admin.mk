TOP_DIR = ..
include ../common.mk

ADMINS_PY = $(addprefix $(ADMIN_DIR)/, $(notdir $(SPECS_JSON:.json=_admin.py)))

$(shell mkdir -p $(ADMIN_DIR))

all : admin

admin : $(ADMINS_PY)

$(ADMIN_DIR)/%_admin.py : $(SPEC_DIR)/%.json $(SCHEMA_JSON)
	amcli genadmin -l $(TEMPLATE_DIR) -o $@ -s $(SCHEMA_JSON) $<

clean :
	rm -f $(ADMINS_PY)

