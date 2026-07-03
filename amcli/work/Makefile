TOP_DIR = ..
include $(TOP_DIR)/common.mk

all : init
	
init : startproject startapp installapp edit

startproject :
	@if [ ! -e manage.py ]; then \
		django-admin startproject $(PROJECT) .; \
	else \
		echo "SKIP: startproject"; \
	fi

startapp :
	@if [ ! -d $(APPLICATION) ]; then \
		python3 manage.py startapp $(APPLICATION); \
	else \
		echo "SKIP: startapp"; \
	fi

installapp :
	amcli installapp \
        --export-installed-apps $(WORK_DIR)/$(PROJECT)/installed_apps.yml \
        --project $(WORK_DIR)/$(PROJECT)/
	amcli installapp \
        --replace-installed-apps $(WORK_DIR)/$(PROJECT)/installed_apps.yml \
        --project $(WORK_DIR)/$(PROJECT)/
	
	amcli installapp rest_framework    --project $(WORK_DIR)/$(PROJECT)/
	amcli installapp django_extensions --project $(WORK_DIR)/$(PROJECT)/
	amcli installapp $(APPLICATION)    --project $(WORK_DIR)/$(PROJECT)/

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

migrate :
	rm -f db.sqlite3
	python3 manage.py makemigrations
	python3 manage.py migrate
	env $$(grep -v '^#' $(TOP_DIR)/.env | xargs) \
	python3 manage.py createsuperuser --noinput || true

loaddata :
	@models=`cat $(SCHEMA_JSON) | jq -r '.load_order[]' | tr '[:upper:]' '[:lower:]'`; \
	for model in $${models}; do \
		fixture=$(TOP_DIR)/tests/data/$${model}_fixture.yaml; \
		python3 manage.py loaddata $${fixture}; \
	done

start :
	@set -a; . $(TOP_DIR)/.env; set +a; \
	rm -f nohup.out; \
	nohup python3 manage.py runserver_plus \
		--cert-file $(TOP_DIR)/$${CERTFILE} $${SERVER_ADDR_PORT} &

stop :
	-pkill -f 'python3 manage.py runserver_plus'

restart : stop start

clean :
	rm -f manage.py
	rm -rf $(PROJECT)
	rm -rf $(APPLICATION)
	rm -f db.sqlite3
	rm -f nohup.out
	rm -rf $(SCHEMA_DIR) $(SPEC_DIR)

