
#SCHEMA = v6.json
SCHEMA = v5.json
#OUTPUT_MODEL_TYPE = dataclasses.dataclass
OUTPUT_MODEL_TYPE = pydantic_v2.BaseModel
#OUTPUT_MODEL_TYPE = typing.TypedDict

all : generate test

prepare :
	python3 -m pip install -r requirements.txt

fetch :
	curl -s -O https://vega.github.io/schema/vega/$(SCHEMA)

generate :
	datamodel-codegen \
		--input $(SCHEMA) --input-file-type jsonschema \
		--disable-timestamp \
		--output-model-type $(OUTPUT_MODEL_TYPE) \
		--output tests/vega.py
	cd tests && patch -p0 -i 0001-fix_default_errors.patch
	cd tests && patch -p0 -i 0002-fix_regex.patch

test :
	cd tests && pytest


