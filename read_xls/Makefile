PYTHON = PYTHONIOENCODING=utf-8 python3

XLSFILES = $(wildcard *.xls)
XLSXFILES = $(wildcard *.xlsx)

all :
	$(PYTHON) read_xls.py -o sample.txt sample.xlsx
	$(PYTHON) read_xls.py -o old_format.txt old_format.xls

clean :
	rm -f sample.txt

