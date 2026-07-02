TOP_DIR = ..
include ../common.mk

SERIALIZERS_PY = $(addprefix $(SERIALIZER_DIR)/, $(notdir $(SPECS_JSON:.json=_serializer.py)))

$(shell mkdir -p $(SERIALIZER_DIR))

all : serializer

serializer : $(SERIALIZERS_PY)

$(SERIALIZER_DIR)/%_serializer.py : $(SPEC_DIR)/%.json
	amcli genserializer -l $(TEMPLATE_DIR) -o $@ -s $(SCHEMA_JSON) $<

clean :
	rm -f $(SERIALIZERS_PY)

