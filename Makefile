
.PHONY: all clean vidserver vidupdate nodeget cleaner

ROOT=$(CURDIR)
DATA=/data/media/vids
REALDATA ?= /data/media/0/realdata
THIRD_PARTY=$(ROOT)/thirdparty

nodejslink=https://nodejs.org/dist/v19.2.0/node-v19.2.0-linux-arm64.tar.xz
npm_cache=/data/media/.npm
nodejstxz=$(THIRD_PARTY)/node-v19.2.0-linux-arm64.tar.xz
nodejsdir=$(THIRD_PARTY)/node-v19.2.0-linux-arm64
webfstgz=$(THIRD_PARTY)/webfs-1.21.tar.gz
webfsdir=$(THIRD_PARTY)/webfs-1.21/
webfs=$(webfsdir)/webfsd

all: $(webfs) $(DATA)

$(nodejsdir):
	(cd $(THIRD_PARTY); wget $(nodejslink))
	(cd $(THIRD_PARTY); tar -xf $(nodejstxz))
	$(RM) $(nodejstxz)
nodeget:$(nodejsdir)

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
			bash -c "source $(ROOT)/env.sh; cd $(DATA); camconcat $(REALDATA) $$route $$i"; \
		done \
	done

vidserver:$(webfs) $(DATA)
	sudo $(webfs) -4 -F -p 80 -r $(DATA)

clean:
	$(RM) -r $(webfsdir)
	$(RM) $(nodejstxz)
	$(RM) -r $(nodejsdir)

cleaner: clean
	$(RM) -r $(DATA)
	$(RM) -r $(npm_cache)
