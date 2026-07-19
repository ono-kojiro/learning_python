TOP_DIR = ..
include ../common.mk

SERIALIZERS_PY = $(addprefix $(SERIALIZER_DIR)/, $(notdir $(SPECS_JSON:.json=_serializer.py)))
	
GENERATOR = $(TOP_DIR)/tools/generate_serializer.py

$(shell mkdir -p $(SERIALIZER_DIR))

all : serializer

serializer : $(SERIALIZERS_PY)

$(SERIALIZER_DIR)/%_serializer.py : $(SPEC_DIR)/%.json
	python3 $(GENERATOR) -s $(SCHEMA_JSON) -r $< -o $@

clean :
	rm -f $(SERIALIZERS_PY)

