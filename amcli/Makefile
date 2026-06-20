#ENTITIES = Device NetIF Comment Manager Remark
ENTITIES = device netif comment manager remark

PROJECT = myproject
APP     = myapp

IN_SPEC_DIR  = specs
WORK_DIR     = work
OUT_SPEC_DIR = $(WORK_DIR)/specs
SCHEMA_DIR   = $(WORK_DIR)/schema

SPEC_YAML = $(addprefix $(IN_SPEC_DIR)/, $(ENTITIES:=.yml))
SPEC_JSON := $(addprefix $(OUT_SPEC_DIR)/, $(notdir $(SPEC_YAML:.yml=.json)))
	
SCHEMA_JSON = $(SCHEMA_DIR)/schema.json

MODEL_DIR = $(WORK_DIR)/$(APP)/models
ADMIN_DIR = $(WORK_DIR)/$(APP)/admin
VIEW_DIR = $(WORK_DIR)/$(APP)/views
SERIALIZER_DIR = $(WORK_DIR)/$(APP)/serializers
FIXTURE_DIR = tests/data

MODEL_PY  = $(addprefix $(MODEL_DIR)/, $(notdir $(ENTITIES:=_model.py)))
ADMIN_PY  = $(addprefix $(ADMIN_DIR)/, $(notdir $(ENTITIES:=_admin.py)))
VIEW_PY   = $(addprefix $(VIEW_DIR)/,  $(notdir $(ENTITIES:=_view.py)))
SERIALIZER_PY = $(addprefix $(SERIALIZER_DIR)/,  $(notdir $(ENTITIES:=_serializer.py)))
FIXTURE_YML = $(addprefix $(FIXTURE_DIR)/test_, $(notdir $(ENTITIES:=-fixtures.yaml)))
	
TEMPLATE_DIR = template
	
$(shell mkdir -p $(OUT_SPEC_DIR))
$(shell mkdir -p $(SCHEMA_DIR))
$(shell mkdir -p $(VIEW_DIR))
$(shell mkdir -p $(SERIALIZER_DIR))
$(shell mkdir -p $(FIXTURE_DIR))

all : cmp2ref schema model admin view serializer fixture

help :
	@echo "usage: make TARGET"
	@echo "  target:"
	@echo "    prepare"
	@echo "    init / cmp2ref / schema / model"

prepare :
	python3 -m pip install -r requirements.txt

init :
	rm -rf $(WORK_DIR)
	amcli startproject $(PROJECT) --dir $(WORK_DIR)/
	amcli startapp     $(APP) --dir $(WORK_DIR)/
	amcli installapp   $(APP) --project $(WORK_DIR)/$(PROJECT)/
	mkdir -p $(OUT_SPEC_DIR)
	mkdir -p $(MODEL_DIR)

debug :
	@echo SPEC_YAML is $(SPEC_YAML)
	@echo SPEC_JSON is $(SPEC_JSON)
	@echo MODEL_DIR is $(MODEL_DIR)
	@echo MODEL_PY is $(MODEL_PY)
	@echo OUT_SPEC_DIR is $(OUT_SPEC_DIR)
	@echo FIXTURE_YML is $(FIXTURE_YML)

cmp2ref : $(SPEC_JSON)

$(OUT_SPEC_DIR)/%.json : $(IN_SPEC_DIR)/%.yml
	amcli cmp2ref --spec $< -o $@ $(SPEC_YAML)

schema :
	amcli genschema -o $(SCHEMA_JSON) $(OUT_SPEC_DIR)/*.json

model: $(MODEL_PY)

$(MODEL_DIR)/%_model.py : $(OUT_SPEC_DIR)/%.json
	amcli genmodel -l $(TEMPLATE_DIR) -o $@ $<

admin: $(ADMIN_PY)

$(ADMIN_DIR)/%_admin.py : $(OUT_SPEC_DIR)/%.json
	amcli genadmin -o $@ -l $(TEMPLATE_DIR) -s $(SCHEMA_JSON) $<

view : $(VIEW_PY)

$(VIEW_DIR)/%_view.py : $(OUT_SPEC_DIR)/%.json
	amcli genview -o $@ -l $(TEMPLATE_DIR) $<

serializer : $(SERIALIZER_PY)

$(SERIALIZER_DIR)/%_serializer.py : $(OUT_SPEC_DIR)/%.json
	amcli genserializer -o $@ -l $(TEMPLATE_DIR) -s $(SCHEMA_JSON) $<

fixture: $(FIXTURE_YML)

$(FIXTURE_DIR)/test_%-fixtures.yaml : $(OUT_SPEC_DIR)/%.json
	amcli genfixture -o $@ -l $(TEMPLATE_DIR) -s $(SCHEMA_JSON) \
		-n template/names.yaml $<

clean :
	rm -f $(SPEC_JSON)
	rm -f $(MODEL_PY)
	rm -f $(ADMIN_PY)
	rm -f $(VIEW_PY)
	rm -f $(SERIALIZER_PY)
	rm -f $(FIXTURE_YML)

mclean :
	rm -rf work

