PROJECT = myproject
APPLICATION = myapp

COMPONENTS = models admin views serializers

SPEC_DIR   = $(TOP_DIR)/specs
SPECS_YML  = $(wildcard $(SPEC_DIR)/*.yml)

SPECS_JSON = $(addprefix $(SPEC_DIR)/, $(notdir $(SPECS_YML:.yml=.json)))

SCHEMA_DIR  = $(TOP_DIR)/schema
SCHEMA_JSON = $(SCHEMA_DIR)/schema.json

ADMIN_DIR = $(TOP_DIR)/admins

VIEW_DIR  = $(TOP_DIR)/views

SERIALIZER_DIR = $(TOP_DIR)/serializers

FIXTURE_DIR = $(TOP_DIR)/fixtures

IMPORTER_DIR = $(TOP_DIR)/importers

TEMPLATE_DIR = $(TOP_DIR)/templates

WORK_DIR = $(TOP_DIR)/work

MODEL_DIR = $(TOP_DIR)/models
MODELS_PY = $(addprefix $(MODEL_DIR)/, $(notdir $(SPECS_JSON:.json=_model.py)))

ALLOWED_HOSTS_YML = $(WORK_DIR)/$(PROJECT)/allowed_hosts.yml

TEST_DIR = $(TOP_DIR)/tests

