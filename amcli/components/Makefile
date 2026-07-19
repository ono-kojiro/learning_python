TOP_DIR = ..
include $(TOP_DIR)/common.mk

all : init spec schema model through \
	admin view serializer dashboard project_urls \
	fixture importer testschema

init :
	$(MAKE) -f init.mk

spec : init
	$(MAKE) -f spec.mk

schema: spec
	$(MAKE) -f schema.mk | tee schema.log

through: schema
	$(MAKE) -f through.mk

testschema: schema
	$(MAKE) -f testschema.mk

model : spec schema
	$(MAKE) -f model.mk

admin : spec schema
	$(MAKE) -f admin.mk

view : spec
	$(MAKE) -f view.mk

serializer : spec schema
	$(MAKE) -f serializer.mk 2>&1 | tee serializer.log

dashboard : spec schema
	$(MAKE) -f dashboard.mk

project_urls : spec schema
	$(MAKE) -f project_urls.mk

fixture : spec schema testschema
	$(MAKE) -f fixture.mk

importer : schema
	$(MAKE) -f importer.mk

clean :
	$(MAKE) -f dashboard.mk  clean
	$(MAKE) -f testschema.mk clean
	$(MAKE) -f importer.mk   clean
	$(MAKE) -f fixture.mk    clean
	$(MAKE) -f serializer.mk clean
	$(MAKE) -f view.mk       clean
	$(MAKE) -f admin.mk      clean
	$(MAKE) -f model.mk      clean
	$(MAKE) -f through.mk    clean
	$(MAKE) -f schema.mk     clean
	$(MAKE) -f spec.mk       clean

