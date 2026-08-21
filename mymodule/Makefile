TOP_DIR = $(shell pwd)

ENV_NAME = myenv

ACTIVATE = . $(TOP_DIR)/$(ENV_NAME)/bin/activate
PYTHON   = $(ACTIVATE) && python3

all : test package
	
prepare :
	sudo apt -y install \
		python3-pip python3-venv \
		python3-pytest python3-dotenv \
		python3-build

env :
	if [ ! -d "$(ENV_NAME)" ]; then \
		python3 -m venv $(ENV_NAME); \
	fi

	$(PYTHON) -m pip install -r requirements.txt

module-list :
	$(PYTHON) -m pip list

package :
	$(PYTHON) -m build

install :
	$(PYTHON) -m pip install -e .

test : pytest

pytest :
	cd tests && $(PYTHON) -m pytest

.PHONY : \
	all clean test build

