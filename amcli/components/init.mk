TOP_DIR = ..
include $(TOP_DIR)/common.mk

all : init
	
init :
	components="$(COMPONENTS)"; \
	for component in $${components}; do \
		mkdir -p $(WORK_DIR)/$(APPLICATION)/$${component}/ ; \
		rm -rf   $(WORK_DIR)/$(APPLICATION)/$${component}.py ; \
	done

