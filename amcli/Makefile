ifneq (,$(wildcard .env))
  include .env
  export $(shell sed 's/=.*//' .env)
endif

#ENTITIES = Device NetIF Comment Manager Remark
ENTITIES = device netif ipv4 comment manager remark

TOP_DIR = $(shell pwd)

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
	
ALLOWED_HOSTS_YML = $(WORK_DIR)/$(PROJECT)/allowed_hosts.yml
	
URLS_API_PY     = $(WORK_DIR)/$(APP)/urls_api.py
LOADER_PY = $(WORK_DIR)/$(APP)/loader.py
APPS_PY = $(WORK_DIR)/$(APP)/apps.py
MODELS_INIT_PY = $(WORK_DIR)/$(APP)/models/__init__.py

TEMPLATE_DIR = template
	

all : cmp2ref schema generate migrate loaddata

init : startproject startapp installapp edit

generate : generate-init model admin view serializer fixture importer

importer : url loader apps models_init

shell :
	cd $(WORK_DIR) && python3 manage.py shell

help :
	@echo "usage: make TARGET"
	@echo "  target:"
	@echo "    prepare"
	@echo "    init / cmp2ref / schema / model"

prepare :
	python3 -m pip install -r requirements.txt

startproject-orig :
	django-admin startproject $(PROJECT) work

startapp-orig :
	cd $(WORK_DIR) && python manage.py startapp $(APP)

startproject :
	amcli startproject $(PROJECT) --dir $(WORK_DIR)/

startapp :
	amcli startapp     $(APP) --dir $(WORK_DIR)/

installapp :
	amcli installapp \
		--export-installed-apps work/myproject/installed_apps.yml \
		--project $(WORK_DIR)/$(PROJECT)/
	amcli installapp \
		--replace-installed-apps work/myproject/installed_apps.yml \
		--project $(WORK_DIR)/$(PROJECT)/
	
	amcli installapp rest_framework    --project $(WORK_DIR)/$(PROJECT)/
	amcli installapp django_extensions --project $(WORK_DIR)/$(PROJECT)/
	amcli installapp $(APP) --project $(WORK_DIR)/$(PROJECT)/
	
	mkdir -p $(OUT_SPEC_DIR)
	mkdir -p $(MODEL_DIR)
	mkdir -p $(VIEW_DIR)
	mkdir -p $(SERIALIZER_DIR)
	mkdir -p $(OUT_SPEC_DIR)
	mkdir -p $(SCHEMA_DIR)
	mkdir -p $(FIXTURE_DIR)

edit :
	amcli edit --export $(ALLOWED_HOSTS_YML) \
		--project $(WORK_DIR)/$(PROJECT) ALLOWED_HOSTS
	
	echo "[ \"*\" ]" > $(ALLOWED_HOSTS_YML)
	
	amcli edit --import $(ALLOWED_HOSTS_YML) \
		--project $(WORK_DIR)/$(PROJECT) ALLOWED_HOSTS
	
	urls_py="$(WORK_DIR)/$(PROJECT)/urls.py"; \
	target="from django.urls import path, include"; \
	grep -q "$$target" $$urls_py || \
	sed -i "s/from django.urls import path/$$target/" $$urls_py; \
	grep -q "path('api/', include('myapp.urls_api'))" $$urls_py || \
	sed -i "/^]/i\    path('api/', include('myapp.urls_api'))," $$urls_py


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

schema : $(SCHEMA_JSON)

$(SCHEMA_JSON) :
	amcli genschema -o $@ \
		--project $(PROJECT) \
		--application $(APP) \
		$(SPEC_JSON)

generate-init :
	components="models admin views serializers"; \
	for component in $${components}; do \
		mkdir -p $(WORK_DIR)/$(APP)/$${component}/ ; \
    	rm -rf   $(WORK_DIR)/$(APP)/$${component}.py ; \
  	done

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


url : $(URLS_API_PY)

$(URLS_API_PY) : template/urls.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

loader : $(LOADER_PY)

$(LOADER_PY) : template/loader.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

apps: $(APPS_PY)

$(APPS_PY) : template/apps.py.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $<

models_init : $(MODELS_INIT_PY)

$(MODELS_INIT_PY) : template/models_init.j2 $(SCHEMA_JSON)
	amcli genimporter -o $@ -s $(SCHEMA_JSON) $< 

migrate :
	rm -f $(WORK_DIR)/db.sqlite3
	cd $(WORK_DIR) && python3 manage.py makemigrations
	cd $(WORK_DIR) && python3 manage.py migrate

	cd $(WORK_DIR) && \
		env $$(grep -v '^#' $(TOP_DIR)/.env | xargs) \
		python3 manage.py createsuperuser --noinput || true

loaddata :
	@models=`cat work/schema/schema.json | jq -r '.load_order[]' | tr '[:upper:]' '[:lower:]'`; \
	echo "MODELS: $${models}"; \
	cd work; \
	for model in $${models}; do \
		echo $${model}; \
		fixture=$(TOP_DIR)/tests/data/test_$${model}-fixtures.yaml; \
		echo $${fixture}; \
		python3 manage.py loaddata $${fixture}; \
	done 

start :
	@set -a; . ./.env; set +a; \
	cd $(WORK_DIR); \
	rm -f nohup.out; \
	nohup python3 manage.py runserver_plus \
      --cert-file $(TOP_DIR)/$${CERTFILE} $${SERVER_ADDR_PORT} &
	head nohup.out

stop :
	pkill -f 'python3 manage.py runserver_plus'

restart : stop start

status :
	ps -ef | grep 'python3 manage.py runserver_plus'

clean :
	rm -f $(SPEC_JSON)
	rm -f $(MODEL_PY)
	rm -f $(ADMIN_PY)
	rm -f $(VIEW_PY)
	rm -f $(SERIALIZER_PY)
	rm -f $(FIXTURE_YML)
	rm -f $(URLS_API_PY) $(LOADER_PY) $(APPS_PY) $(MODELS_INIT_PY)

mclean :
	rm -rf work

