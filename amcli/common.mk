PROJECT = myproject
APPLICATION = myapp

COMPONENTS = models admin views serializers

WORK_DIR = $(TOP_DIR)/work

INPUT_DIR   = $(TOP_DIR)/specs
SPEC_DIR   = $(WORK_DIR)/specs

SPECS_YML  = $(wildcard $(INPUT_DIR)/*.yml)
SPECS_JSON = $(addprefix $(SPEC_DIR)/, $(notdir $(SPECS_YML:.yml=.json)))

SCHEMA_DIR  = $(WORK_DIR)/schema
SCHEMA_JSON = $(SCHEMA_DIR)/schema.json

TESTSCHEMA_DIR  = $(WORK_DIR)/schema
TESTSCHEMA_JSON = $(SCHEMA_DIR)/testschema.json


IMPORTER_DIR = $(TOP_DIR)/importers

TEMPLATE_DIR = $(TOP_DIR)/templates



#MODEL_DIR = $(TOP_DIR)/models
MODEL_DIR = $(WORK_DIR)/$(APPLICATION)/models

MODELS_PY = $(addprefix $(MODEL_DIR)/, $(notdir $(SPECS_JSON:.json=_model.py)))

#ADMIN_DIR = $(TOP_DIR)/admins
ADMIN_DIR = $(WORK_DIR)/$(APPLICATION)/admin

#VIEW_DIR  = $(TOP_DIR)/views
VIEW_DIR  = $(WORK_DIR)/$(APPLICATION)/views

#SERIALIZER_DIR = $(TOP_DIR)/serializers
SERIALIZER_DIR = $(WORK_DIR)/$(APPLICATION)/serializers/

#FIXTURE_DIR = $(TOP_DIR)/fixtures
FIXTURE_DIR = $(TEST_DIR)/data


ALLOWED_HOSTS_YML = $(WORK_DIR)/$(PROJECT)/allowed_hosts.yml

TEST_DIR = $(TOP_DIR)/tests

