TOP_DIR = ..
include ../common.mk

PROJECT_URLS_PY = $(PROJECT_DIR)/urls.py

all : projecturls

projecturls : $(PROJECT_URLS_PY)

$(PROJECT_URLS_PY) : $(SCHEMA_JSON)
	amcli genprojecturls -o $@ -l $(TEMPLATE_DIR) -s $<

clean :
	rm -f $(PROJECT_URLS_PY)

