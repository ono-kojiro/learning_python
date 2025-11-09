PYTHONPATH = ..

CONFIG = ../config.shrc
API_KEY = ../api_key.shrc
PYTHON = PYTHONPATH=$(PYTHONPATH) python3

all : list

list :
	$(PYTHON) show_models.py --api-key $(API_KEY) --config $(CONFIG)

help :
	@echo "usage: make TARGET"
	@echo ""
	@echo "target:"
	@echo "  list"

