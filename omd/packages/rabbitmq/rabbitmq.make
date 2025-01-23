RABBITMQ := rabbitmq

RABBITMQ_BUILD := $(BUILD_HELPER_DIR)/$(RABBITMQ)-build
RABBITMQ_INSTALL := $(BUILD_HELPER_DIR)/$(RABBITMQ)-install
RABBITMQ_BAZEL_OUT := $(BAZEL_BIN_EXT)/$(RABBITMQ)

.PHONY: $(RABBITMQ_BUILD)
$(RABBITMQ_BUILD):
	$(BAZEL_CMD) build @$(RABBITMQ)//:build

.PHONY: $(RABBITMQ_INSTALL)
$(RABBITMQ_INSTALL): $(RABBITMQ_BUILD)
	$(RM) $(DESTDIR)$(OMD_ROOT)/lib/rabbitmq
	tar -xzf $(RABBITMQ_BAZEL_OUT)/rabbitmq.tar.gz -C $(DESTDIR)$(OMD_ROOT)/lib/
	install -m 755 $(PACKAGE_DIR)/$(RABBITMQ)/RABBITMQ_PORT $(DESTDIR)$(OMD_ROOT)/lib/omd/hooks/
	install -m 755 $(PACKAGE_DIR)/$(RABBITMQ)/RABBITMQ_MANAGEMENT_PORT $(DESTDIR)$(OMD_ROOT)/lib/omd/hooks/
	install -m 755 $(PACKAGE_DIR)/$(RABBITMQ)/RABBITMQ_DIST_PORT $(DESTDIR)$(OMD_ROOT)/lib/omd/hooks/
	install -m 755 $(PACKAGE_DIR)/$(RABBITMQ)/RABBITMQ_ONLY_FROM $(DESTDIR)$(OMD_ROOT)/lib/omd/hooks/
