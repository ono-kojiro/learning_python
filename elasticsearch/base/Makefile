PASSWORD = $(shell cat ../.netrc | grep password | gawk '{ print $$2 }')
PASSWORD = $(shell cat ../.netrc | grep password | gawk '{ print $$2 }')

all :
	./es_version.py

http :
	curl -n http://localhost:9200/

https :
	curl -n https://localhost:9200/

create :
	python3 create_index.py myindex

