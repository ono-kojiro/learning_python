PYTHONPATH = ..

CONFIG = ../config.shrc
API_KEY = ../api_key.shrc
PYTHON = PYTHONPATH=$(PYTHONPATH) python3

COLLECTION = myknowledge
MODEL = mymodel
QUERY = "Linuxとは何ですか? また、Windowsとは何が異なるのですか？"
#MODEL = hf.co/Falfredplpl/Fgemma-2-baku-2b-it-gguf:latest

all : chat

help :
	@echo "usage: make TARGET"
	@echo ""
	@echo "target:"
	@echo "  chat"

chat:
	$(PYTHON) chat.py --api-key $(API_KEY) --config $(CONFIG) \
		-m "$(MODEL)" -q $(QUERY)	--collection "$(COLLECTION)"

