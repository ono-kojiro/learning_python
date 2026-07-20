TOP_DIR = ..
include ../common.mk

ADMINS_PY = $(addprefix $(ADMIN_DIR)/, $(notdir $(SPECS_JSON:.json=_admin.py)))
GENERATOR = $(TOP_DIR)/tools/generate_admin.py

# remove
NESTED_ADMIN_PY = $(APP_DIR)/admin/__init__.py

$(shell mkdir -p $(ADMIN_DIR))

all : admin nestedadmin init

admin : $(ADMINS_PY)

$(ADMIN_DIR)/%_admin.py : $(SCHEMA_JSON)
	python3 $(GENERATOR) -o $@ -m $* $<

nestedadmin: $(NESTED_ADMIN_PY)

$(NESTED_ADMIN_PY) : $(SCHEMA_JSON)
	amcli gennestedadmin -l $(TEMPLATE_DIR) -o $@ -s $(SCHEMA_JSON)

init :
	python3 $(TOP_DIR)/tools/generate_admin_init.py \
		-o $(NESTED_ADMIN_PY) $(SCHEMA_JSON)

clean :
	rm -f $(ADMINS_PY)
	rm -f $(NESTED_ADMIN_PY)


