TOP_DIR = ..
include $(TOP_DIR)/common.mk

URLS_API_PY = $(WORK_DIR)/$(APPLICATION)/urls_api.py
LOADER_PY   = $(WORK_DIR)/$(APPLICATION)/loader.py
APPS_PY     = $(WORK_DIR)/$(APPLICATION)/apps.py
MODELS_INIT_PY = $(WORK_DIR)/$(APPLICATION)/models/__init__.py

all : url apps models_init

url : $(URLS_API_PY)

loader : $(LOADER_PY)

apps : $(APPS_PY)

models_init : $(MODELS_INIT_PY)

$(URLS_API_PY) : $(TEMPLATE_DIR)/urls.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

$(LOADER_PY) : $(TEMPLATE_DIR)/loader.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

$(APPS_PY) : $(TEMPLATE_DIR)/apps.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

$(MODELS_INIT_PY) : $(TEMPLATE_DIR)/models_init.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

clean :
	rm -f $(URLS_API_PY)
	rm -f $(LOADER_PY)
	rm -f $(APPS_PY)
	rm -f $(MODELS_INIT_PY)

