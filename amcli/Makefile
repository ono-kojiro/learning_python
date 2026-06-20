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

MODEL_PY  = $(addprefix $(MODEL_DIR)/, $(notdir $(ENTITIES:=_model.py)))
ADMIN_PY  = $(addprefix $(ADMIN_DIR)/, $(notdir $(ENTITIES:=_admin.py)))
	
$(shell mkdir -p $(OUT_SPEC_DIR))
$(shell mkdir -p $(SCHEMA_DIR))

all : cmp2ref schema model admin

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

cmp2ref : $(SPEC_JSON)

$(OUT_SPEC_DIR)/%.json : $(IN_SPEC_DIR)/%.yml
	amcli cmp2ref --spec $< -o $@ $(SPEC_YAML)

schema :
	amcli genschema -o $(SCHEMA_JSON) $(OUT_SPEC_DIR)/*.json

model: $(MODEL_PY)

$(MODEL_DIR)/%_model.py : $(OUT_SPEC_DIR)/%.json
	amcli genmodel -l template/ -o $@ $<

admin: $(ADMIN_PY)

$(ADMIN_DIR)/%_admin.py : $(OUT_SPEC_DIR)/%.json
	amcli genadmin -o $@ -l template/ -s $(SCHEMA_JSON) $<

mclean :
	rm -rf work

