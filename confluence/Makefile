#URL = https://cwiki.apache.org/confluence/display/SVN/Apache+Subversion+Wiki
URL = https://cwiki.apache.org/confluence/

all : page

page :
	python3 get_page.py -u $(URL) -o page.json

spaces :
	python3 get_spaces.py -u $(URL) -o output.json


