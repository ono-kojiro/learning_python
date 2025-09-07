
#SCHEMA = v6.json
SCHEMA_JSON  = v5.json
SCHEMA_URL   = https://vega.github.io/schema/vega/$(SCHEMA_JSON)

#OUTPUT_MODEL_TYPE = dataclasses.dataclass
OUTPUT_MODEL_TYPE = pydantic_v2.BaseModel
#OUTPUT_MODEL_TYPE = typing.TypedDict

SPEC_JSON = Spec.json
SPEC_URL = https://raw.githubusercontent.com/PBI-David/Deneb-Showcase/refs/heads/main/Force%20Directed%20Graph/$(SPEC_JSON)

all : generate test

prepare :
	python3 -m pip install -r requirements.txt

fetch :
	curl -s --output-dir tests/ -O $(SCHEMA_URL)
	curl -s --output-dir tests/ -O $(SPEC_URL)

generate :
	datamodel-codegen \
		--input tests/$(SCHEMA_JSON) --input-file-type jsonschema \
		--disable-timestamp \
		--output-model-type $(OUTPUT_MODEL_TYPE) \
		--output tests/vega.py
	cd tests && patch -p0 -i 0001-fix_default_errors.patch
	cd tests && patch -p0 -i 0002-fix_regex.patch
	cd tests && patch -p0 -i 0003-fix_stroke_type.patch
	cd tests && patch -p0 -i 0004-fix_encode_entry.patch

test :
	$(MAKE) -C tests


