HTMLFILES = 57228_58735.html 56680_62855.html 56669_58756.html 56689_63891.html
TEXTFILES = $(HTMLFILES:.html=.txt)
JSONFILES = $(TEXTFILES:.txt=.ndjson)

ENCODED   = ZGxhZzhKMEI0bmtmYkpqZGx1ZFA6TWk5ZW1EblRFejdfZ1YwRUtkNWt4dw==

all : text json

fetch:
	for filename in $(HTMLFILES); do \
		if [ ! -e "$${filename}" ]; then \
			wget https://www.aozora.gr.jp/cards/001779/files/$${filename}; \
		else \
			echo "Skip $${filename}"; \
		fi \
	done

text : $(TEXTFILES)

json : $(JSONFILES)

%.txt : %.html
	html2text -o $@ $<

%.ndjson : %.txt
	python3 txt2ndjson.py -o $@ $<

test : prepare-vector prepare-query query

prepare-vector :
	python3 txt2ndjson.py -o vector.json query.txt

prepare-query :
	jq --slurpfile vec vector.json \
  		'.knn.query_vector = $$vec[0].vector' \
  		template.json > query.json
  		
#'.query.script_score.script.params.query_vector = $$vec[0].vector' \

query :
	@curl -X POST "https://192.168.1.72:9200/embeddings-*/_search?pretty" \
		-H "Authorization: ApiKey $(ENCODED)" \
		-H "Content-Type: application/json" \
		--data-binary @query.json

check:
	curl -X GET "https://192.168.1.72:9200/embeddings-*/_mapping?pretty" \
		-H "Authorization: ApiKey $(ENCODED)" \

clean :
	rm -f $(TEXTFILES) $(JSONFILES)

