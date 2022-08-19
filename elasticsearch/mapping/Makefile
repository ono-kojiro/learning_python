.SUFFIX:

USERNAME = "elastic"
PASSWORD = "8x*qe+eOKaMK-o+DakO*"

all : mapping post

test : search

mapping :
	curl \
  -k \
  -u $(USERNAME):$(PASSWORD) \
  -H "Content-Type: application/json" \
  -XPUT "https://192.168.0.98:9200/employee" \
  --data-binary @mappings.json

post :
	curl \
  -k \
  -u $(USERNAME):$(PASSWORD) \
  -H "Content-Type: application/json" \
  -XPOST "https://192.168.0.98:9200/employee/_doc" \
  --data-binary @data.json

search :
	curl \
  -k \
  -u $(USERNAME):$(PASSWORD) \
  -H "Content-Type: application/json" \
  -XGET "https://192.168.0.98:9200/employee/_search?pretty" \
  --data-binary @search.json

clean :
	curl \
  -k \
  -u $(USERNAME):$(PASSWORD) \
  -H "Content-Type: application/json" \
  -XDELETE "https://192.168.0.98:9200/employee"

.PHONY : \
    all clean test search

