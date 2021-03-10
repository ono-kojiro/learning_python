INPUT_DIR = input
OUTPUT_DIR = output

INPUTS = $(wildcard $(INPUT_DIR)/*.doc)
OUTPUTS = $(addprefix $(OUTPUT_DIR)/, $(notdir $(INPUTS)))

$(shell mkdir -p $(OUTPUT_DIR))

all : merge format

output : $(OUTPUTS)


format :
	python3 format.py -o all.doc merged.doc

merge :
	python3 merge.py -o tmp.doc $(INPUTS)
	cat header.html tmp.doc footer.html > merged.doc

test :
	python3 merge.py -o tmp.html input/00-Managing_the_Subversion_Project.doc
	cat header.html tmp.html footer.html > all.doc

