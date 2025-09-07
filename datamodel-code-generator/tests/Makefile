all : test

test :
	pytest
	sed -i -e 's/"as_"/"as"/' output.json
	sed -i -e 's/"from_"/"from"/' output.json
	sed -i -e 's/"field_schema"/"$$schema"/' output.json
	cat output.json | jq 'del(..|nulls)' > tmp.json
	mv -f tmp.json output.json

