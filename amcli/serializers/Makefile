TOP_DIR = ..
include ../common.mk

SERIALIZERS_PY = $(addprefix $(SERIALIZER_DIR)/, $(notdir $(SPECS_JSON:.json=_serializer.py)))

all : serializer copy

serializer : $(SERIALIZERS_PY)

$(SERIALIZER_DIR)/%_serializer.py : $(SPEC_DIR)/%.json
	amcli genserializer -l $(TEMPLATE_DIR) -o $@ -s $(SCHEMA_JSON) $<

copy :
	mkdir -p $(WORK_DIR)/$(APPLICATION)/serializers
	cp -f $(SERIALIZERS_PY) $(WORK_DIR)/$(APPLICATION)/serializers/

clean :
	rm -f $(SERIALIZERS_PY)

