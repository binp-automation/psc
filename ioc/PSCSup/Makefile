TOP=..
include $(TOP)/configure/CONFIG
#=======================================

# Build devPSC as a library for an IOC:
LIBRARY_$(APP_ARCH) += devPSC
LIBRARY = $(LIBRARY_$(T_A))

# Library includes
devPSC_INCLUDES += -I$(APP_SRC_DIR)/src

# Library Source files
devPSC_SRCS += \
	devPSC.cpp

# Link with the libraries
devPSC_LIBS += $(EPICS_BASE_IOC_LIBS)

# Workaround to link shared library
ifeq ($(APP_FAKEDEV),)
	PSC_LDFLAGS += -Wl,-Bdynamic -l:libapp.so
else
	PSC_LIBS += app_fakedev
endif

# Install .dbd and .db files
DBD += devPSC.dbd
DB_INSTALLS += $(TOP)/PSCSup/devPSC.db

#=======================================
include $(TOP)/configure/RULES
