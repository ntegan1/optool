
.PHONY: all clean vidserver vidupdate

ROOT=$(CURDIR)
DATA=/data/media/vids
REALDATA ?= /data/media/0/realdata
THIRD_PARTY=$(ROOT)/thirdparty

webfstgz=$(THIRD_PARTY)/webfs-1.21.tar.gz
webfsdir=$(THIRD_PARTY)/webfs-1.21/
webfs=$(webfsdir)/webfsd

all: $(webfs) $(DATA)

$(DATA):
	mkdir -p $(DATA)

$(webfsdir):$(webfstgz)
	tar -xzf $(webfstgz) -C $(THIRD_PARTY)

$(webfs):$(webfsdir)
	echo ok
	make -C $(webfsdir) config
	bash -c 'sed -iE '"'"'s/^-e \(LIB.*\)$$/\1/'"'"' $(webfsdir)/Make.config'
	make -C $(webfsdir)

routes := $(shell bash -c "source $(ROOT)/env.sh >/dev/null 2>&1 ; lsroute $(REALDATA)")
vidupdate:
	for route in $(routes); do \
		for i in e d f; do \
			echo r $$route $$i; \
			echo ho; \
			bash -c "source $(ROOT)/env.sh; cd $(DATA); camconcat $(REALDATA) $$route $$i"; \
		done \
	done

vidserver:$(webfs)
	$(webfs) -h

clean:
	$(RM) -r $(webfsdir)
