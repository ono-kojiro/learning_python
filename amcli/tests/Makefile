TOP_DIR = ..
include $(TOP_DIR)/common.mk

ENTITIES = $(notdir $(SPECS_JSON:.json=))

# ex.
#   in:  template/test_generated_get.j2
#   out:    tests/test_generated_get_device.py
#
TEST_TEMPLATES_J2 = \
    $(TEMPLATE_DIR)/test_generated_get.j2 \
    $(TEMPLATE_DIR)/test_generated_create.j2 \
    $(TEMPLATE_DIR)/test_generated_delete.j2 \
    $(TEMPLATE_DIR)/test_generated_update.j2

TEST_SCRIPTS_PY = $(foreach tmpl,$(TEST_TEMPLATES_J2), \
                    $(foreach e,$(ENTITIES), \
                      ./$(basename $(notdir $(tmpl)))_$(e).py))

all : gentest

debug :
	@echo $(ENTITIES)

gentest : $(TEST_SCRIPTS_PY)

gentest : $(TEST_SCRIPTS_PY)

define GENTEST_RULE
$(1)_rule:
./$(basename $(notdir $(1)))_%.py : $(1)
	amcli gentest \
		--schema $(SCHEMA_JSON) \
		--ref $(SPEC_DIR)/$$*.json \
		--output $$@ \
		$$<
endef

# 各テンプレートに対してルールを生成
$(foreach tmpl,$(TEST_TEMPLATES_J2),$(eval $(call GENTEST_RULE,$(tmpl))))

clean :
	rm -f $(TEST_SCRIPTS_PY)
	rm -f test_generated_*.py

