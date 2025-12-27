OUTDIR   = .
TEMPLATE = templates/template.json.jinja
#OUTPUT = $(addprefix $(OUTDIR)/, $(notdir $(TEMPLATE:.jinja=)))
OUTPUT = output.json

all :
	python3 generate.py -o $(OUTPUT) $(TEMPLATE)

debug :
	python3 generate.py -d -o $(OUTPUT) $(TEMPLATE)

