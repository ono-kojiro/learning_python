include .env

INDEX = embeddings-default-2026.05.10

all : test

query :
	python3 str2vector.py -o query.json $(TEXT)

test :
	curl -X POST "https://192.168.1.72:9200/$(INDEX)/_search?pretty" \
		-H "Content-Type: application/json" \
		-H "Authorization: ApiKey $(ENCODED)" \
		-d @query.json | tee result.json
