TOP_DIR = ..
include ../common.mk

DASHBOARD_PY = $(APP_DIR)/dashboard.py

all : dashboard

dashboard : $(DASHBOARD_PY)

$(DASHBOARD_PY) : $(SCHEMA_JSON)
	amcli gendashboard -o $@ -l $(TEMPLATE_DIR) -s $<

clean :
	rm -f $(DASHBOARD_PY)

