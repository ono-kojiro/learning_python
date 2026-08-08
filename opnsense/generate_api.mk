TOP_DIR = ..

include controllers.mk
include $(TOP_DIR)/variables.mk

all : api

api : $(APIS_PY)

$(API_DIR)/%.py : $(SPEC_DIR)/%.yml
	mkdir -p `dirname $@`
	python3 $(TOP_DIR)/yml2py.py -o $@ $<

