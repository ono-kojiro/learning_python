TOP_DIR = ..
include $(TOP_DIR)/common.mk

URLS_API_PY = urls_api.py
LOADER_PY   = loader.py
APPS_PY     = apps.py
MODELS_INIT_PY = models_init.py

all : init url loader apps models_init copy

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

init :
	components="$(COMPONENTS)"; \
	for component in $${components}; do \
		mkdir -p $(WORK_DIR)/$(APPLICATION)/$${component}/ ; \
		rm -rf   $(WORK_DIR)/$(APPLICATION)/$${component}.py ; \
	done

copy :
	cp -f $(URLS_API_PY) $(WORK_DIR)/$(APPLICATION)/
	cp -f $(LOADER_PY)   $(WORK_DIR)/$(APPLICATION)/
	cp -f $(APPS_PY)     $(WORK_DIR)/$(APPLICATION)/
	cp -f $(MODELS_INIT_PY) $(WORK_DIR)/$(APPLICATION)/models/__init__.py

clean :
	rm -f $(URLS_API_PY)
	rm -f $(LOADER_PY)
	rm -f $(APPS_PY)
	rm -f $(MODELS_INIT_PY)

