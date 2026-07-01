TOP_DIR = ..
include ../common.mk

ADMINS_PY = $(addprefix $(ADMIN_DIR)/, $(notdir $(SPECS_JSON:.json=_admin.py)))

all : admin copy

admin : $(ADMINS_PY)

$(ADMIN_DIR)/%_admin.py : $(SPEC_DIR)/%.json
	amcli genadmin -l $(TEMPLATE_DIR) -o $@ -s $(SCHEMA_JSON) $<

copy :
	mkdir -p $(WORK_DIR)/$(APPLICATION)/admin
	cp -f $(ADMINS_PY) $(WORK_DIR)/$(APPLICATION)/admin/

clean :
	rm -f $(ADMINS_PY)

