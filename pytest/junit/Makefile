PYTEST = pytest-3

all :
	$(PYTEST) --junit-xml=junit_report.xml

install :
	python3 -m pip install -r requirements.txt

test :
	pytest --tap-stream | tappy

clean :
	rm -rf __pycache__

