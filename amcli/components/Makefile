TOP_DIR = ..
include $(TOP_DIR)/common.mk

all : spec schema model admin view serializer fixture importer testschema

spec :
	$(MAKE) -f spec.mk

schema:
	$(MAKE) -f schema.mk

testschema:
	$(MAKE) -f testschema.mk

model :
	$(MAKE) -f model.mk

admin :
	$(MAKE) -f admin.mk

view :
	$(MAKE) -f view.mk

serializer :
	$(MAKE) -f serializer.mk

fixture :
	$(MAKE) -f fixture.mk

importer :
	$(MAKE) -f importer.mk

clean :
	$(MAKE) -f importer.mk   clean
	$(MAKE) -f fixture.mk    clean
	$(MAKE) -f serializer.mk clean
	$(MAKE) -f view.mk       clean
	$(MAKE) -f admin.mk      clean
	$(MAKE) -f model.mk      clean
	$(MAKE) -f schema.mk     clean
	$(MAKE) -f spec.mk       clean


