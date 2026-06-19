ENTITIES = Device NetIF Comment Manager Remark

IN_SPEC_DIR  = specs
WORK_DIR     = work
OUT_SPEC_DIR = $(WORK_DIR)/specs

SPEC_YAML = $(addprefix $(IN_SPEC_DIR)/, $(ENTITIES:=.yml))
SPEC_JSON = $(addprefix $(OUT_SPEC_DIR)/, $(notdir $(SPEC_YAML:.yml=.json)))
	
$(shell mkdir -p $(OUT_SPEC_DIR))

all : init cmp2ref

prepare :
	python3 -m pip install -r requirements.txt

init :
	rm -rf $(WORK_DIR)
	mkdir -p $(OUT_SPEC_DIR)
	amcli startproject myproject --dir work/
	amcli startapp     myapp --dir work/
	amcli installapp   myapp --project work/myproject/

cmp2ref : $(SPEC_JSON)

$(OUT_SPEC_DIR)/%.json : $(IN_SPEC_DIR)/%.yml
	amcli cmp2ref --name $* -o $@ specs/*.yml

mclean :
	rm -rf work

