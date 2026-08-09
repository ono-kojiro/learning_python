SOURCE_DIR = ./source
SPEC_DIR   = $(TOP_DIR)/spec
API_DIR    = $(TOP_DIR)/src

SPECS_YML = $(subst $(SOURCE_DIR),$(SPEC_DIR),$(CONTROLLERS_PHP:controller.php=.yml))

APIS_PY = $(subst $(SPEC_DIR),$(API_DIR),$(SPECS_YML:.yml=.py))


