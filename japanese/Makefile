PYTHON = python3

INPUT=日本語のテキスト.txt

all :
	PYTHONIOENCODING=utf-8 $(PYTHON) read_text.py -o output.txt $(INPUT)
	$(PYTHON) jaconv_test.py input.txt

clean :
	rm -f output.txt

