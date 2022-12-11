
.PHONY: all clean vidserver vidupdate nodeget cleaner nginxget nginx \
	nginxrun nginxstop nginxreload nginxquit

ROOT=$(CURDIR)
DATA=/data/media/vids
REALDATA ?= /data/media/0/realdata
THIRD_PARTY=$(ROOT)/thirdparty

nginxlink=https://nginx.org/download/nginx-1.22.1.tar.gz
nginxtgz=$(THIRD_PARTY)/nginx-1.22.1.tar.gz
nginxdir=$(THIRD_PARTY)/nginx-1.22.1
nginxexe=$(nginxdir)/objs/nginx
nginxrtmplink=https://github.com/arut/nginx-rtmp-module
nodejslink=https://nodejs.org/dist/v19.2.0/node-v19.2.0-linux-arm64.tar.xz
npm_cache=/data/media/.npm
nodejstxz=$(THIRD_PARTY)/node-v19.2.0-linux-arm64.tar.xz
nodejsdir=$(THIRD_PARTY)/node-v19.2.0-linux-arm64
webfstgz=$(THIRD_PARTY)/webfs-1.21.tar.gz
webfsdir=$(THIRD_PARTY)/webfs-1.21/
webfs=$(webfsdir)/webfsd

all: $(webfs) $(DATA)

$(nginxdir):
	(cd $(THIRD_PARTY); wget $(nginxlink))
	(cd $(THIRD_PARTY); tar -xf $(nginxtgz))
	$(RM) $(nginxtgz)
nginxget:$(nginxdir)
	(cd $(nginxdir); git clone $(nginxrtmplink))
$(nginxexe):
	(cd $(nginxdir); ./configure --with-http_ssl_module --with-http_v2_module --with-stream=dynamic --with-http_addition_module --with-http_mp4_module --add-module=nginx-rtmp-module; make -j2; mkdir -p logs)

nginx:$(nginxdir) $(nginxexe)

nginxrun:
	sudo $(nginxexe) -p $(nginxdir)
nginxstop:
	sudo $(nginxexe) -p $(nginxdir) -s quit
nginxquit:
	sudo $(nginxexe) -p $(nginxdir) -s quit
nginxreload:
	sudo $(nginxexe) -p $(nginxdir) -s reload

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
	$(RM) $(nginxtgz)
	$(RM) -r $(nginxdir)

cleaner: clean
	$(RM) -r $(DATA)
	$(RM) -r $(npm_cache)
