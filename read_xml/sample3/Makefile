PYTHON = python3

all : text json

text :
	$(PYTHON) read_xls.py -o mybook.txt mybook.xlsx
	cat mybook.txt

json :
	$(PYTHON) read_text.py -o mybook.json mybook.txt
	cat mybook.json

parse :
	$(PYTHON) read_xml.py \
		-o output.txt \
		-s schema.xsd \
		example.xml

clean :
	rm -f output.txt

