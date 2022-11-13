all :
	python3 setup.py bdist_wheel

install :
	pip3 install dist/xml2jsonl-0.0.1-py3-none-any.whl

test :
	python3 -m pytest --junit-xml=tmp.xml
	cat tmp.xml | xmllint --format - > junit_report.xml
	cat junit_report.xml

check : test

uninstall :
	pip3 uninstall xml2jsonl

.PHONY : \
    all clean test install uninstall

